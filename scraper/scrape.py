from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
from bs4 import BeautifulSoup
import requests
import sys, traceback
import threading
import warnings
import MySQLdb as mysql
import progressbar

url = "https://duapp2.drexel.edu/webtms_du/app"
terms = {}
professors = []
counter = 0

def search(term, name="", crn="", number=""):
    #gotta have some search term
    if name == "" and crn == "" and number == "":
        return []

    #connect and get the results page
    data = get_search_data(term, name=name, crn=crn, number=number)
    r = session.post(url, data, cookies={'JSESSIONID': 'EBDD6180F7190A6FE19518E71A592A66'})
    result = BeautifulSoup(r.text, "lxml")

    #check to make sure session is still good
    if result.title.get_text() == "Stale Session":
        print "Session is stale. Please provide new session ID"
        sys.exit(-1)

    #parse the results
    table = result.find("table", bgcolor="cccccc")
    rows = table.find_all("tr", recursive=False)
    results = []
    for tr in rows:
        if tr.find("td").get_text() == "Subject Code":
            continue
        try:
            row = parse_row(tr)
            row['term'] = term
            results.append(row)
        except: #last row causes an issue, because it's just filler
            continue
    return results

def get_term_number(term):
    #try and avoid re-getting the term number
    t = terms.get(term, None)
    if t is not None:
        return t

    #term isn't in cache, search for it and add it
    tms_main = BeautifulSoup(session.get(url).text, "lxml")
    term_list = tms_main.find("select", id="term", class_="formField")
    for option in term_list.find_all("option"):
        if option.getText() == term:
            terms[term] = option['value']
            return option['value']


def get_search_data(term, name='', number='', crn=''):
    return {
        'formids': 'term,courseName,crseNumb,crn',
        'component': 'searchForm',
        'page': 'Home',
        'service': 'direct',
        'submitmode': 'submit',
        'submitname': '',
        'term': get_term_number(term),
        'courseName': name,
        'crseNumb': number,
        'crn': crn
    }


def parse_row(tablerow):
    data = tablerow.findAll("td")
    #for i in range(0, len(data)):
        #print 'col %d: %s' % (i, data[i])
    listing = {
        'name': data[0].getText()+data[1].getText(),
        'type': data[2].getText(),
        'sec': "%s\n%s" % (data[7].getText(), data[8].getText()),
        'CRN': data[4].getText(),
        'title': data[5].getText(),

        'instructor': data[-1].getText().split(', '),
    }
    return listing

def create_session():
    global session
    session = requests.Session()

def create_connection():
    global conn
    conn = mysql.connect(host='localhost',
                         user='root',
                         passwd='root',
                         db='declassified')
    global cur
    cur = conn.cursor()
    with warnings.catch_warnings():
        #suppress "table already exists" warnings
        warnings.filterwarnings('ignore', 'Table \'[a-z]*\' already exists')
        cur.execute('CREATE TABLE IF NOT EXISTS professors(\
                    name VARCHAR(50) NOT NULL, \
                    rating DECIMAL(2,1), \
                    tags VARCHAR(255), \
                    PRIMARY KEY (name));')
        cur.execute('CREATE TABLE IF NOT EXISTS classes(\
                    code VARCHAR(10) NOT NULL,\
                    name VARCHAR(255) NOT NULL,\
                    section VARCHAR(255) NOT NULL,\
                    professor VARCHAR(50) NOT NULL,\
                    type VARCHAR(255) NOT NULL,\
                    term VARCHAR(255) NOT NULL,\
                    crn INT NOT NULL,\
                    PRIMARY KEY (crn),\
                    FOREIGN KEY (professor) REFERENCES professors(name));')


def db_insert(info):
    prof_statement = "INSERT IGNORE INTO professors (name) VALUES %s"
    profs = ""
    for p in info['instructor']:
        if p not in professors:
            profs += "(\"%s\")," % p
            professors.append(p)
    if profs != "":
        prof_statement = (prof_statement % profs)[0:-1] + ';' #trim trailing , and append ;
        db_execute(prof_statement)
    
    class_statement = "INSERT IGNORE INTO classes\
            (code, name, section, type, crn, professor, term)\
            VALUES (%s, %s, %s, %s, %s, %s, %s);"
    for p in info['instructor']:
        db_execute(class_statement, (info['name'], info['title'],info['sec'], info['type'], info['CRN'], p, info['term']))

#wrapper function to handle DB timeout
def db_execute(query, params=None):
    try:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
    except mysql.OperationalError:
        create_connection()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)

class scrapeThread(threading.Thread):
    def __init__(self, term, start, end, bar):
        threading.Thread.__init__(self)
        self.st = start
        self.en = end
        self.term = term
        self.bar = bar
    def run(self):
        global counter
        global professors
        for i in range(self.st, self.en):
            results = search(self.term, number=i)
            for c in results:
                db_insert(c)
            if len(professors) > 1000:
                professors = []
            counter = counter + 1
            self.bar.update(counter)
        conn.commit()

if __name__ == "__main__":
    create_session()
    create_connection()
    threads = []

    thread_count = 5
    min_count = 0
    max_count = 1000
    bar = progressbar.ProgressBar(max_value=max_count-min_count)
    for i in range(0, thread_count):
        scrape_range = (max_count-min_count)/thread_count
        newThread = scrapeThread("Winter Quarter 16-17", i*scrape_range+min_count, (i+1)*scrape_range+min_count, bar)
        newThread.start()
        threads.append(newThread)

    for thread in threads:
        thread.join()
    conn.commit()
    conn.close()
import MySQLdb as mysql
from bs4 import BeautifulSoup
import requests
import time
import progressbar

def create_connection():
    global conn
    conn = mysql.connect(host='localhost',
                         user='root',
                         passwd='root',
                         db='declassified')
    global cur
    cur = conn.cursor()

def get_search_url(name):
    return "http://www.ratemyprofessors.com/search.jsp?queryoption=HEADER&queryBy=teacherName&schoolName=Drexel+University&schoolID=&query=" + name.replace(' ', '+')

def get_prof_url(session, url):
    r = session.get(url)
    results = BeautifulSoup(r.text, "lxml")
    prof = results.find("li", {"class": "listing PROFESSOR"})
    if prof is not None:
        prof = prof.find("a")['href']
        return "http://www.ratemyprofessors.com/" + prof
    return prof

def search_prof(session, url):
    r = session.get(url)
    results = BeautifulSoup(r.text, "lxml")
    try:
        rating = float(results.find("div", {"class": "grade"}).contents[0])
    except: #professor has no ratings
        return (0, '')
    tags_div = results.findAll("span", {"class": "tag-box-choosetags"})
    tags = []
    if tags_div is not None:
        for tag in tags_div:
            tag_name = tag.contents[0].strip()
            tag_freq = tag.contents[1].contents[0]
            tags.append("%s" % (tag_name))
    if tags:
        tags = reduce((lambda x, y: '%s,%s' %(x,y) if len('%s,%s' %(x,y)) < 255 else x), tags)
    return (rating, tags)

def insert_prof(name, rating, tags):
    query = 'UPDATE professors SET rating=%s, tags=%s WHERE name=%s;'
    args = (rating, tags, name)
    query = query % conn.literal(args)
    cur.execute(query)

def main():
    create_connection()
    cur.execute('SELECT name FROM professors;')
    professors = []
    for row in cur.fetchall():
        professors.append(row[0])
    
    session = requests.Session()
    min = 0
    max = len(professors)
    bar = progressbar.ProgressBar(max_value=max-min)
    complete = 0
    for prof in professors[min:max]:
        search_url = get_search_url(prof)
        prof_url = get_prof_url(session, search_url)
        if prof_url is not None:
            results = search_prof(session, prof_url)
            insert_prof(prof, results[0], str(results[1]))
        else:
            insert_prof(prof, 0, '')
        complete += 1
        bar.update(complete)
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    main()
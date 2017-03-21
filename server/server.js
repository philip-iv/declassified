var express = require('express');
var app = express();
var path = require('path');
var mysql = require('mysql');
var con = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'root',
    database: 'declassified'
});

con.connect(function(err) {
    if (err) {
        console.log("error");
    }
    else {
        console.log("connected");
    }
});

app.use(express.static(__dirname + "/../client"));
app.listen(8080, '0.0.0.0', function() {
  console.log("Server running");
});

app.get('/all', function(req, res){
    con.query('\
    SELECT code, classes.name, section, professor, crn, rating, tags FROM classes \
    INNER JOIN professors \
    WHERE classes.professor = professors.name AND \
    professors.rating > 0 \
    ORDER BY professors.rating DESC, professors.name ASC\
    ;\
    ', function(err, rows, fields) {
        if (err)
            console.log(err);
        else {
            res.send(rows);
        }
    });
});

# -*- coding:utf-8 -*-
from flask import Flask,render_template
import MySQLdb as mysql
import json

try:
    conn = mysql.connect(host='host',user='user',passwd='pass',db='spider_chart',port=3306)
    cur=conn.cursor()
except mysql.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])




app = Flask(__name__)

@app.route('/<group_name>')

def index(group_name):
    return render_template('index.html',group_name=group_name)

@app.route('/groups')

def groups():
    sql = 'select group_name from groups'
    cur.execute(sql)
    arr = []
    for i in cur.fetchall():
        arr.append([i[0]])
    return json.dumps(arr)


@app.route('/data/<group_name>')

def data(group_name):
    global cur
    sql = 'select time_hour,auto_check_count,no_check_count from cms_pull_logs where group_name="%s"' % (group_name)
    cur.execute(sql)
    arr = []
    for i in cur.fetchall():
        arr.append([i[0]*1000,i[1]+i[2]])
    return json.dumps(arr)





if __name__=='__main__':
    app.run(host='0.0.0.0',port=9092,debug=True)

# -*- coding:utf-8 -*-
from flask import Flask,render_template
import ConfigParser
import MySQLdb as mysql
import json

#载入数据库配置信息
cf = ConfigParser.ConfigParser()
cf.read("config/common.ini")
db_host = cf.get("db","db_host")
db_port = cf.get("db","db_port")
db_user = cf.get("db","db_user")
db_pass = cf.get("db","db_pass")
db_database = cf.get("db","db_database")

try:
    conn = mysql.connect(host=db_host,user=db_user,passwd=db_pass,db=db_database,port=int(db_port))
    cur=conn.cursor()
except mysql.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])




app = Flask(__name__)

#查看每个频道图表展现的路由
@app.route('/<group_name>')
def index(group_name):
    return render_template('index.html',group_name=group_name)


#获取所有推送频道的路由
@app.route('/groups')
def groups():
    sql = 'select group_name from groups'
    cur.execute(sql)
    arr = []
    for i in cur.fetchall():
        arr.append([i[0]])
    return json.dumps(arr)


#获取每个频道推送数据的路由
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

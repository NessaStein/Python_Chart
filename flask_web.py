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

app = Flask(__name__)


def mysql_conn():
    try:
        conn = mysql.connect(host=db_host,user=db_user,passwd=db_pass,db=db_database,port=int(db_port))
        return conn.cursor()
    except mysql.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

#查看每个频道图表展现的路由
@app.route('/<group_name>')
def index(group_name):
    return render_template('index.html',group_name=group_name)


#获取所有推送频道的路由
@app.route('/groups')
def groups():
    cur = mysql_conn()
    sql = 'select group_name from groups'
    cur.execute(sql)
    arr = []
    for i in cur.fetchall():
        arr.append([i[0]])
    return json.dumps(arr)


#获取每个频道推送数据的路由
@app.route('/data/<group_name>/<tag>')
def data(group_name,tag):
    cur = mysql_conn()
    tag_list = ['cmspull','spiderpush','spidergrab']
    arr = []
    if tag in tag_list:
        if tag == 'cmspull':
            pull_sql = 'select time_hour,auto_check_count,no_check_count from cms_pull_logs where group_name="%s"' % (group_name)
            cur.execute(pull_sql)
            for i in cur.fetchall():
                arr.append([i[0]*1000,i[1]+i[2]])

        if tag == 'spiderpush':
            push_sql = 'select time_hour,sum(push_count) as push_count from spider_push_logs where group_name="%s" group by time_hour' % (group_name)
            cur.execute(push_sql)
            for j in cur.fetchall():
                arr.append([j[0]*1000,int(j[1])])

        if tag == 'spidergrab':
            grab_sql = 'select time_hour,grab_count from spider_grab_logs where group_name="%s"' % (group_name)
            cur.execute(grab_sql)
            for k in cur.fetchall():
                arr.append([k[0]*1000,k[1]])


    return json.dumps(arr)



if __name__=='__main__':
    app.run(host='0.0.0.0',port=9092,debug=True)

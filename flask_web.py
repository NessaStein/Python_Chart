# -*- coding:utf-8 -*-

import ConfigParser
import json

import MySQLdb as mysql
from flask import Flask, render_template

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

#欢迎页路由
@app.route('/')
def welcome():
    return render_template('welcome/index.html')


#每个频道图表展现路由
@app.route('/<group_name>')
def index(group_name):
    return render_template('spider/index.html',group_name=group_name)

#nodejs缩图监路由
@app.route('/nodejs_thumb_img')
def nodejs_thumb_img():
    thumb_data = get_nodejs_thumb_log(10)
    thumb_sort_data = get_nodejs_thumb_log_sort(10)
    return render_template('nodejs/index.html',thumb_data=thumb_data,thumb_sort_data=thumb_sort_data)

#nodejs缩图百分比更多页面
@app.route('/nodejs_thumb_img_percent_more')
def nodejs_thumb_img_percent_more():
    thumb_data = get_nodejs_thumb_log(1000)
    return render_template('nodejs/percent_more.html',thumb_data=thumb_data)

#nodejs缩图倒序更多页面
@app.route('/nodejs_thumb_img_sort_more')
def nodejs_thumb_img_sort_more():
    thumb_sort_data = get_nodejs_thumb_log_sort(1000)
    return render_template('nodejs/sort_more.html',thumb_sort_data=thumb_sort_data)


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



#得到NodeJs一周内缩图后比原图还要大的日志数据
def get_nodejs_thumb_log(limit):
    if limit == '':
        limit = 10
    cur = mysql_conn()
    node_thumb_sql = 'select dt,thumb_size,pic_size,thumb_width,thumb_height,pic_width,pic_height,percentage,thumb_url,pic_url from nodejs_thumb_log where percentage>100 and UNIX_TIMESTAMP(dt) >= UNIX_TIMESTAMP()-604800 and UNIX_TIMESTAMP(dt)<=UNIX_TIMESTAMP() group by thumb_url order by percentage desc limit 0,%d' % limit
    cur.execute(node_thumb_sql)
    arr = []
    for i in cur.fetchall():
        thumb_size = format_bit(i[1])
        pic_size = format_bit(i[2])
        arr.append([i[0],thumb_size,pic_size,i[3],i[4],i[5],i[6],i[7],i[8],i[9]])
    return arr

#nodejs一周内原图从大到小排序
def get_nodejs_thumb_log_sort(limit):
    if limit == '':
        limit = 10
    cur = mysql_conn()
    node_thumb_sort_sql = 'select dt,thumb_size,pic_size,thumb_width,thumb_height,pic_width,pic_height,percentage,thumb_url,pic_url from nodejs_thumb_log where UNIX_TIMESTAMP(dt) >= UNIX_TIMESTAMP()-604800 and UNIX_TIMESTAMP(dt)<=UNIX_TIMESTAMP() group by thumb_url  order by pic_size desc limit 0,%d' % limit
    cur.execute(node_thumb_sort_sql)
    arr = []
    for i in cur.fetchall():
        thumb_size = format_bit(i[1])
        pic_size = format_bit(i[2])
        arr.append([i[0],thumb_size,pic_size,i[3],i[4],i[5],i[6],i[7],i[8],i[9]])
    return arr

#字节码转换
def format_bit(size):
    if size/1024<1:
        return str(size) + 'B'
    if size/1024/1024<1:
        d = str(size/1024) + '.' + str(size%1024)
        return str(float('%.1f'% float(d))) + 'K'
    if size/1024/1024/1024<1:
        d = str(size/1024/1024) + '.' + str(size/1024%1024)
        return str(float('%.1f' % float(d))) + 'M'


if __name__=='__main__':
    app.run(host='0.0.0.0',port=9092,debug=True)

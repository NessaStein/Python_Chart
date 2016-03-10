# -*- coding:utf-8 -*-
import os
import re
import time
import MySQLdb as mysql
import ConfigParser

#载入数据库配置信息
cf = ConfigParser.ConfigParser()
cf.read("config/common.ini")
db_host = cf.get("db","db_host")
db_port = cf.get("db","db_port")
db_user = cf.get("db","db_user")
db_pass = cf.get("db","db_pass")
db_database = cf.get("db","db_database")

#载入火车头抓取数据库配置信息
spider_db_host = cf.get("spider_db","spider_db_host")
spider_db_port = cf.get("spider_db","spider_db_port")
spider_db_user = cf.get("spider_db","spider_db_user")
spider_db_pass = cf.get("spider_db","spider_db_pass")
spider_db_database = cf.get("spider_db","spider_db_database")

#载入信息接口
cms_interface_url = cf.get("cms_interface","cms_interface_url")
cms_interface_key = cf.get("cms_interface","cms_interface_key")

try:
    conn = mysql.connect(host=db_host,user=db_user,passwd=db_pass,db=db_database,port=int(db_port))
    cur=conn.cursor()
except mysql.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])

try:
    spider_conn = mysql.connect(host=spider_db_host,user=spider_db_user,passwd=spider_db_pass,db=spider_db_database,port=int(spider_db_port))
    spider_cur=spider_conn.cursor()
except mysql.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])


#获取当时时间和时间戳
now_time = time.strftime('%Y-%m-%d %H',time.localtime(time.time()))
now_time_all = now_time + ':00:00'
timeArray = time.strptime(now_time_all, "%Y-%m-%d %H:%M:%S")
timeStamp = int(time.mktime(timeArray))


#md5函数
def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

#CMS分类和频道对应关系接口
def getGroupInfoByCateId(cid):
    if cid:
        if cid !=0:
            import requests,json
            key = cms_interface_key
            ymd = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            s = md5(key+ymd)
            #获得CMS分类和频道信息
            group_categoryid_info_url = cms_interface_url+'?id='+str(cid)+'&s='+s
            r = requests.get(group_categoryid_info_url)
            return r.text

#分析推送数量
def sync_push_log():
    global timeStamp
    sql = "select count(id) as count,cmstypeid from new_send_log where state !=3 and cmstypeid is not null and createtime like('%s%%') group by cmstypeid" % now_time
    spider_cur.execute(sql)
    for i in spider_cur.fetchall():
        if i[1]:
            if i[1]!=0:
                group_name = getGroupInfoByCateId(i[1])
                if group_name:
                    insert_spider_push_logs(group_name,timeStamp,i[0],i[1])

#分析火车头抓取数量
def sync_grab_log():
    global timeStamp
    up_sql_clear = 'delete from spider_grab_logs where time_hour=%s' % timeStamp
    cur.execute(up_sql_clear)
    conn.commit

    sql = "select count(*) as count,nt.chinaType from newinfo ni,newstype nt where ni.type=nt.name and ni.inTime  like('%s%%') group by chinaType" % now_time
    spider_cur.execute(sql)
    for i in spider_cur.fetchall():
        if i[1]:
            group_name = getGroupInfoByCateId(i[1])
            if group_name:
                insert_spider_grab_logs(group_name,timeStamp,i[0])

#插入推送统计表
def insert_spider_push_logs(group_name,timeStamp,push_count,category_id):
    sql = "select * from spider_push_logs where group_name='%s' and time_hour=%s and category_id=%s" % (group_name,timeStamp,category_id)
    cur.execute(sql)
    result=cur.fetchone()
    if result:
        up_sql = 'update spider_push_logs set push_count=%s where group_name=\'%s\' and time_hour=%s and category_id=%s' % (push_count,group_name,timeStamp,category_id)
        cur.execute(up_sql)
    else:
        in_sql = 'insert into spider_push_logs (group_name,time_hour,push_count,category_id) VALUES (\'%s\',%s,%s,%s)' % (group_name,timeStamp,push_count,category_id)
        cur.execute(in_sql)
    conn.commit()

#插入抓取统计表
def insert_spider_grab_logs(group_name,timeStamp,grab_count):
    sql = "select * from spider_grab_logs where group_name='%s' and time_hour=%s" % (group_name,timeStamp)
    cur.execute(sql)
    result=cur.fetchone()
    if result:
        up_sql = 'update spider_grab_logs set grab_count=grab_count+%s where group_name=\'%s\' and time_hour=%s' % (grab_count,group_name,timeStamp)
        cur.execute(up_sql)
    else:
        in_sql = 'insert into spider_grab_logs (group_name,time_hour,grab_count) VALUES (\'%s\',%s,%s)' % (group_name,timeStamp,grab_count)
        cur.execute(in_sql)
    conn.commit()

#调用推送分析
sync_push_log()
#调用抓取量分析
sync_grab_log()
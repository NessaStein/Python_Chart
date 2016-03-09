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

try:
    conn = mysql.connect(host=db_host,user=db_user,passwd=db_pass,db=db_database,port=int(db_port))
    cur=conn.cursor()
except mysql.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])


#日志文件检索
def seachFiles(path,world):
    for filename in os.listdir(path):
        fp = os.path.join(path,filename)
        if os.path.isfile(fp) and world in filename:
            analyseData(fp)
        elif os.path.isdir(fp):
            seachFiles(fp,world)

#同步日志数据到数据库
def analyseData(log):
    if os.path.isfile(log):
        file_name = os.path.basename(log)
        file_name = file_name.replace('huochetou_','')
        group_name = file_name.replace('.txt','')

        #更新频道到频道表
        if group_name:
            insert_groups(group_name)

        file_info = open(log,'r')
        try:
            log_info = file_info.read()
        finally:
            file_info.close()

        now_time = time.strftime('%Y-%m-%d %H',time.localtime(time.time()))
        now_time_all = now_time + ':00:00'
        timeArray = time.strptime(now_time_all, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        no_check_count = auto_check_count = 0
        pattern = re.findall("(group:"+group_name+"--autocheck:0--dt:"+now_time+")",log_info)
        if(pattern):
            no_check_count = len(pattern)

        pattern = re.findall("(group:"+group_name+"--autocheck:1--dt:"+now_time+")",log_info)
        if(pattern):
            auto_check_count = len(pattern)

        insert_cms_pull_logs(group_name,timeStamp,no_check_count,auto_check_count)


#插入统计表
def insert_cms_pull_logs(group_name,timeStamp,no_check_count,auto_check_count):
    sql = "select * from cms_pull_logs where group_name='"+group_name+"' and time_hour=%s" % timeStamp
    cur.execute(sql)
    result=cur.fetchone()
    if result:
        up_sql = 'update cms_pull_logs set auto_check_count=%s, no_check_count=%s where group_name=\'%s\' and time_hour=%s' % (auto_check_count,no_check_count,group_name,timeStamp)
        cur.execute(up_sql)
    else:
        in_sql = 'insert into cms_pull_logs (group_name,time_hour,auto_check_count,no_check_count) VALUES (\'%s\',%s,%s,%s)' % (group_name,timeStamp,auto_check_count,no_check_count)
        cur.execute(in_sql)
    conn.commit()

#插入频道表
def insert_groups(group_name):
    sql = 'select * from groups where group_name="%s"' % (group_name)
    cur.execute(sql)
    result=cur.fetchone()
    if not result:
        in_sql = 'insert into groups (group_name) VALUES (\'%s\')' % (group_name)
        cur.execute(in_sql)
    conn.commit()

#日志目录
logdir = './logs/'

#日志统计入口
seachFiles(logdir,'huochetou')


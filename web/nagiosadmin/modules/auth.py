#!/usr/bin/env python
#coding:utf8


import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import MySQLdb

def auth(username,password):
    try:
        conn = MySQLdb.connect(host='10.5.8.46',user='monitor_appuser',passwd='ourpalm.com',db='itsm_online',port=3307,charset='utf8')
        cur=conn.cursor()
        cur.execute('select username,password from itsm_users where username="%s"' %username)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
    except MySQLdb.IntegrityError,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

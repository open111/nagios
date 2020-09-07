#!/usr/bin/env python
#coding:utf8


import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import MySQLdb

def query(ip):
    try:
        conn = MySQLdb.connect(host='10.5.8.46',user='monitor_appuser',passwd='ourpalm.com',db='itsm_online',port=3307,charset='utf8')
        cur=conn.cursor()
        cur.execute('''
SELECT
        m.asset_no,
        m.public_ip,
        m.private_ip,
        i.`name` idc_name,
        s.`name` service_name,
        d.dept_name app_dept_name,
        d2.dept_name use_dept_name,
        u.`name` app_use_name,
        m.nagios_status,
        m.nagios_description,
        m.ganglia_status,
        m.ganglia_description,
        m.os,
        m. STATUS,
        m.memo
FROM
        itsm_asset_machine m
LEFT JOIN itsm_services s ON m.service_code = s.`code`                                                                     
LEFT JOIN itsm_asset_dept d ON m.application_dept_id = d.id                                                                
LEFT JOIN itsm_asset_dept d2 ON m.use_dept_id = d2.id                                                                      
LEFT JOIN itsm_users u ON m.applicant_id = u.id                                                                            
LEFT JOIN itsm_users u2 ON m.contacts_id = u2.id                                                                           
LEFT JOIN itsm_asset_idc i ON m.idc_id = i.id                                                                              
WHERE                                                                                                                      
        public_ip="%s" or private_ip="%s"
''' %(ip,ip))
        #ganglia[i[0]] = {'asset_no':i[0],'public_ip':i[1],'private_ip':i[2],'idc_name':i[3],'service_name':i[4],'app_dept_name':i[5],'use_dept_name':i[6],'use_name':i[7],'nagios_status':i[8],'nagios_description':i[9],'ostype':i[10],'status':i[11],'memo':i[12]}
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
    except MySQLdb.IntegrityError,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    #for k in results:
    #    print k


with open('ip') as f:
    counter = 0
    for i in f:
       try:
           d, = query(i.strip())
           print d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9],d[10],d[11]
           counter += 1
       except:
           print d
           counter += 1

print counter

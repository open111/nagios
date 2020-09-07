#!/usr/bin/env python

import os
import sys



def mysql(dict):
    service_name      = dict['service_name']
    service_directory = dict['service_directory']
    idc_name          = dict['idc_name']
    idc_directory     = dict['idc_directory']
    idc_region        = dict['idc_region']
    template          = dict['template']
    host_name         = dict['host_name']
    services_path     = dict['Services']
    private_ip        = dict['private_ip']
    ports             = dict['ports']
    m_type            = dict['m_type']
    
    if private_ip and service_name and service_directory and type \
       and idc_name and idc_directory and idc_region and services_path:
        for port in ports:
            if m_type == 'master':
                m1  = ['define service{\n',
                          '\thost_name           %s\n' %(host_name),
                          '\tservice_description %s\n' %(service_name+'_'+'Check_Mysql_%s' %(port)),
                          '\tdisplay_name        %s\n' %(service_name+'_'+'Check_Mysql_%s' %(port)),
                          '\tuse                 %s\n' %(template),
                          '\tcheck_command       check_mysql!%s\n' %port,
                          '\tregister            1\n',
                          '}\n']
                items = [m1]

            elif m_type == 'slave':
                s1  = ['define service{\n',
                          '\thost_name           %s\n' %(host_name),
                          '\tservice_description %s\n' %(service_name+'_'+'Check_Mysql_%s_%s' %(m_type,port)),
                          '\tdisplay_name        %s\n' %(service_name+'_'+'Check_Mysql_%s_%s' %(m_type,port)),
                          '\tuse                 %s\n' %(template),
                          '\tcheck_command       check_mysql_slavedb!%s!300\n' %port,
                          '\tregister            1\n',
                          '}\n']
                n1 = ['define service{\n',
                          '\thost_name           %s\n' %(host_name),
                          '\tservice_description %s\n' %(service_name+'_'+'Check_Mysql_%s_%s_night' %(m_type,port)),
                          '\tdisplay_name        %s\n' %(service_name+'_'+'Check_Mysql_%s_%s_night' %(m_type,port)),
                          '\tuse                 BJZW_mysql_slave_night\n' ,
                          '\tcheck_command       check_mysql_slavedb!%s!300\n' %port,
                          '\tregister            1\n',
                          '}\n']

                items = [s1,n1]


            ser_path = services_path+'/'+idc_directory+'/'+service_directory
            if os.path.exists(ser_path):
                if not os.path.exists(ser_path+'/'+'mysql'):
                    os.makedirs(ser_path+'/'+'mysql')
                if os.path.exists(ser_path+'/'+'mysql'):
                    f_path = ser_path+'/'+'mysql'+'/'+host_name+'_'+'Mysql_'+m_type+'_'+port+'.cfg'
                    if not os.path.exists(f_path):
                        with open(f_path,'w') as f:
                            for i in items:
                                for x in i:
                                    f.write(x)
                    else:
                        f_path,' existing...'
                else:
                    print ser_path+'/'+'mysql',' Not Found...'
            else:
                print ser_path,' Not Found...'
        

#!/usr/bin/env python

import os
import sys



def redis(dict):
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
                items  = ['define service{\n',
                          '\thost_name           %s\n' %(host_name),
                          '\tservice_description %s\n' %(service_name+'_'+'Check_Redis_%s_%s' %(m_type,port)),
                          '\tdisplay_name        %s\n' %(service_name+'_'+'Check_Redis_%s_%s' %(m_type,port)),
                          '\tuse                 %s\n' %(template),
                          '\tcheck_command       check_redis_mem!"127.0.0.1 %s 65"\n' %port,
                          '\tregister            1\n',
                          '}\n']
            	tcp = ['define service {\n',
                   	  '\thost_name              %s\n' %(host_name),
                     	  '\tservice_description    %s\n' %(service_name+'_'+'Check_Tcp_%s' %(port)),
                  	  '\tdisplay_name           %s\n' %(service_name+'_'+'Check_Tcp_%s' %(port)),
                   	  '\tuse                    ops_redis_p0\n',
                   	  '\tcheck_command          check_tcp!%s\n' %port,
                   	  '\tregister               1\n',
                   	  '}\n']



            elif m_type == 'slave':
                items  = ['define service{\n',
                          '\thost_name           %s\n' %(host_name),
                          '\tservice_description %s\n' %(service_name+'_'+'Check_Redis_%s_%s' %(m_type,port)),
                          '\tdisplay_name        %s\n' %(service_name+'_'+'Check_Redis_%s_%s' %(m_type,port)),
                          '\tuse                 %s\n' %(template),
                          '\tcheck_command       check_redis_slave!"127.0.0.1 %s"\n' %port,
                          '\tregister            1\n',
                          '}\n']
            	tcp = ['define service {\n',
                   	  '\thost_name              %s\n' %(host_name),
                     	  '\tservice_description    %s\n' %(service_name+'_'+'Check_Tcp_%s' %(port)),
                  	  '\tdisplay_name           %s\n' %(service_name+'_'+'Check_Tcp_%s' %(port)),
                   	  '\tuse                    %s\n' %(template),
                   	  '\tcheck_command          check_tcp!%s\n' %port,
                   	  '\tregister               1\n',
                   	  '}\n']



            ser_path = services_path+'/'+idc_directory+'/'+service_directory
            if os.path.exists(ser_path):
                if not os.path.exists(ser_path+'/'+'redis'):
                    os.mkdir(ser_path+'/'+'redis')
                if os.path.exists(ser_path+'/'+'redis'):
                    f_path = ser_path+'/'+'redis'+'/'+host_name+'_'+'Redis_'+m_type+'_'+port+'.cfg'
                    if not os.path.exists(f_path):
                        with open(f_path,'w') as f:
                            for i in items:
                                f.write(i)
                    else:
                        f_path,' existing...'
                    t_path = ser_path+'/'+'redis'+'/'+host_name+'_'+'Redis_'+'tcp'+'_'+port+'.cfg'
                    if not os.path.exists(t_path):
                        with open(t_path,'w') as f:
                            for i in tcp:
                                f.write(i)
                    else:
                        t_path,' existing...'
                else:
                    print ser_path+'/'+'redis',' Not Found...'
            else:
                print ser_path,' Not Found...'
        

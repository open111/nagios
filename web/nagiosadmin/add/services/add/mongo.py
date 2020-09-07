#!/usr/bin/env python

import os
import sys



def mongo(dict):
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
                          '\tservice_description %s\n' %(service_name+'_'+'Check_MongoDB_%s' %(port)),
                          '\tdisplay_name        %s\n' %(service_name+'_'+'Check_MongoDB_%s' %(port)),
                          '\tuse                 %s\n' %(idc_directory+'_'+service_name+'_MongoDB_p0'),
                          '\tcheck_command       check_nrpe!check_mongodb!" -A connect -P %s -W 40 -C 60 -u nagios -p sysadmin@ourpalm"\n' %port,
                          '\tregister            1\n',
                          '}\n']
                l1  = ['define service{\n',
                          '\thost_name           %s\n' %(host_name),
                          '\tservice_description %s\n' %(service_name+'_'+'Check_MongoDB_replset_%s' %(port)),
                          '\tdisplay_name        %s\n' %(service_name+'_'+'Check_MongoDB_replset_%s' %(port)),
                          '\tuse                 %s\n' %(idc_directory+'_'+service_name+'_MongoDB_p1'),
                          '\tcheck_command       check_nrpe!check_mongodb!" -A connect -P %s -A replset_state -u nagios -p sysadmin@ourpalm"\n' %port,
                          '\tregister            1\n',
                          '}\n']
                o1  = ['define service{\n',
                          '\thost_name           %s\n' %(host_name),
                          '\tservice_description %s\n' %(service_name+'_'+'Check_MongoDB_repl_switch_%s' %(port)),
                          '\tdisplay_name        %s\n' %(service_name+'_'+'Check_MongoDB_repl_switch_%s' %(port)),
                          '\tuse                 %s\n' %(idc_directory+'_'+service_name+'_MongoDB_p1'),
                          '\tcheck_command       check_nrpe!check_mongodb!" -A connect -P %s -A mongo_repl_switch -u nagios -p sysadmin@ourpalm"\n' %port,
                          '\tregister            1\n',
                          '}\n']
                items = [m1,l1,o1]

            elif m_type == 'slave':
                p1  = ['define service{\n',
                          '\thost_name           %s\n' %(host_name),
                          '\tservice_description %s\n' %(service_name+'_'+'Check_MongoDB_%s' %(port)),
                          '\tdisplay_name        %s\n' %(service_name+'_'+'Check_MongoDB_%s' %(port)),
                          '\tuse                 %s\n' %(idc_directory+'_'+service_name+'_MongoDB_p0'),
                          '\tcheck_command       check_nrpe!check_mongodb!" -A connect -P %s -W 40 -C 60  -u nagios -p sysadmin@ourpalm"\n' %port,
                          '\tregister            1\n',
                          '}\n']
                q1  = ['define service{\n',
                          '\thost_name           %s\n' %(host_name),
                          '\tservice_description %s\n' %(service_name+'_'+'Check_MongoDB_replset_%s' %(port)),
                          '\tdisplay_name        %s\n' %(service_name+'_'+'Check_MongoDB_replset_%s' %(port)),
                          '\tuse                 %s\n' %(idc_directory+'_'+service_name+'_MongoDB_p1'),
                          '\tcheck_command       check_nrpe!check_mongodb!" -A connect -P %s -A replset_state -u nagios -p sysadmin@ourpalm"\n' %port,
                          '\tregister            1\n',
                          '}\n']
                r1  = ['define service{\n',
                          '\thost_name           %s\n' %(host_name),
                          '\tservice_description %s\n' %(service_name+'_'+'Check_MongoDB_repl_switch_%s' %(port)),
                          '\tdisplay_name        %s\n' %(service_name+'_'+'Check_MongoDB_repl_switch_%s' %(port)),
                          '\tuse                 %s\n' %(idc_directory+'_'+service_name+'_MongoDB_p1'),
                          '\tcheck_command       check_nrpe!check_mongodb!" -A connect -P %s -A mongo_repl_switch -u nagios -p sysadmin@ourpalm"\n' %port,
                          '\tregister            1\n',
                          '}\n']
                items = [p1,q1,r1]


            elif m_type == 'arbiter':
                s1  = ['define service{\n',
                          '\thost_name           %s\n' %(host_name),
                          '\tservice_description %s\n' %(service_name+'_'+'Check_MongoDB_%s' %(port)),
                          '\tdisplay_name        %s\n' %(service_name+'_'+'Check_MongoDB_%s' %(port)),
                          '\tuse                 %s\n' %(idc_directory+'_'+service_name+'_MongoDB_p0'),
                          '\tcheck_command       check_nrpe!check_mongodb!" -A connect -P %s -W 40 -C 60 "\n' %port,
                          '\tregister            1\n',
                          '}\n']
                t1  = ['define service{\n',
                          '\thost_name           %s\n' %(host_name),
                          '\tservice_description %s\n' %(service_name+'_'+'Check_MongoDB_replset_%s' %(port)),
                          '\tdisplay_name        %s\n' %(service_name+'_'+'Check_MongoDB_replset_%s' %(port)),
                          '\tuse                 %s\n' %(idc_directory+'_'+service_name+'_MongoDB_p1'),
                          '\tcheck_command       check_nrpe!check_mongodb!" -A connect -P %s -A replset_state "\n' %port,
                          '\tregister            1\n',
                          '}\n']
                u1  = ['define service{\n',
                          '\thost_name           %s\n' %(host_name),
                          '\tservice_description %s\n' %(service_name+'_'+'Check_MongoDB_repl_switch_%s' %(port)),
                          '\tdisplay_name        %s\n' %(service_name+'_'+'Check_MongoDB_repl_switch_%s' %(port)),
                          '\tuse                 %s\n' %(idc_directory+'_'+service_name+'_MongoDB_p1'),
                          '\tcheck_command       check_nrpe!check_mongodb!" -A connect -P %s -A mongo_repl_switch "\n' %port,
                          '\tregister            1\n',
                          '}\n']
                items = [s1,t1,u1]

            ser_path = services_path+'/'+idc_directory+'/'+service_directory
            if os.path.exists(ser_path):
                if not os.path.exists(ser_path+'/'+'mongo'):
                    os.makedirs(ser_path+'/'+'mongo')
                if os.path.exists(ser_path+'/'+'mongo'):
                    f_path = ser_path+'/'+'mongo'+'/'+host_name+'_'+'Mongo_'+m_type+'_'+port+'.cfg'
                    if not os.path.exists(f_path):
                        with open(f_path,'w') as f:
                            for i in items:
                                for x in i:
                                    f.write(x)
                    else:
                        f_path,' existing...'
                else:
                    print ser_path+'/'+'mongo',' Not Found...'
            else:
                print ser_path,' Not Found...'
        

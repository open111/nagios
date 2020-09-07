#!/usr/bin/env python

import os
import sys



def tcp(dict):
    service_name      = dict['service_name']
    service_directory = dict['service_directory']
    idc_name          = dict['idc_name']
    idc_directory     = dict['idc_directory']
    idc_region        = dict['idc_region']
    template          = dict['template']
    host_name         = dict['host_name']
    services_path     = dict['Services']
    private_ip        = dict['private_ip']
    type              = dict['type']
    ports             = dict['ports']
    
    if private_ip and service_name and service_directory and type\
       and idc_name and idc_directory and idc_region and services_path:
        for port in ports:
            items  = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description %s\n' %(service_name+'_'+'Check_%s_%s' %(type,port)),
                      '\tdisplay_name        %s\n' %(service_name+'_'+'Check_%s_%s' %(type,port)),
                      '\tuse                 %s\n' %(template),
                      '\tcheck_command       check_tcp!%s\n' %port,
                      '\tregister            1\n',
                      '}\n']


            ser_path = services_path+'/'+idc_directory+'/'+service_directory
            if os.path.exists(ser_path):
                if not os.path.exists(ser_path+'/'+'tcp'):
                    os.mkdir(ser_path+'/'+'tcp')
                if os.path.exists(ser_path+'/'+'tcp'):
                    f_path = ser_path+'/'+'tcp'+'/'+host_name+'_'+type+'_'+port+'.cfg'
                    if not os.path.exists(f_path):
                        with open(f_path,'w') as f:
                            for i in items:
                                f.write(i)
                    else:
                        f_path,' existing...'
                else:
                    print ser_path+'/'+'tcp',' Not Found...'
            else:
                print ser_path,' Not Found...'
        

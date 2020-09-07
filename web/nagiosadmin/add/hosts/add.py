#!/usr/bin/env python


import os
import sys


def hosts(dict):
    service_name       = dict['service_name']
    service_directory  = dict['service_directory']
    idc_name           = dict['idc_name']
    idc_directory      = dict['idc_directory']
    idc_region         = dict['idc_region']
    group_name         = dict['group_name']
    group_directory    = dict['group_directory']
    public_ip          = dict['public_ip']
    private_ip         = dict['private_ip']
    hosts_path         = dict['Hosts']
    hostgroups_path    = dict['Hostgroups']
    services_path      = dict['Services']


    if public_ip or private_ip and service_name and idc_region:
        if public_ip and private_ip:
            host_name = idc_region+'_'+service_name+'_'+public_ip
            #ip = private_ip
	    ip = public_ip
        elif public_ip:
            host_name = idc_region+'_'+service_name+'_'+public_ip
            ip = public_ip
        else:
            host_name = idc_region+'_'+service_name+'_'+private_ip
            ip = private_ip
        
        items = ['define host{\n',
                '\thost_name   %s\n' %(host_name),
                '\talias       %s\n' %(host_name),
                '\taddress     %s\n' %(ip),
                '\tuse         %s\n' %(idc_region+'_'+service_name+'_'+'hosttemplate,hosts-pnp'),
                '\tregister    1\n',
                '}\n',]


        templa = ['define host {\n',
                  '\tname                         %s\n' %(idc_region+'_'+service_name+'_'+'hosttemplate'),
                  '\talias                        %s\n' %(idc_region+'_'+service_name+'_'+'hosttemplate'),
                  '\tcheck_command                check-host-alive\n',
                  '\tmax_check_attempts           2\n',
                  '\tcheck_interval               2\n',
                  '\tretry_interval               1\n',
                  '\tcheck_period                 24x7\n',
                  '\tevent_handler_enabled        1\n',
                  '\tflap_detection_enabled       1\n',
                  '\tprocess_perf_data            1\n',
                  '\tretain_status_information    1\n',
                  '\tretain_nonstatus_information 1\n',
                  '\tcontact_groups               ops-p0\n',
                  '\tnotification_interval        60\n',
                  '\tnotification_period          24x7\n',
                  '\tnotification_options         d,u,r\n',
                  '\tnotifications_enabled        1\n',
                  '\tfailure_prediction_enabled   1\n',
                  '\tregister                     0\n',
                  '}\n',]


    if service_directory and idc_name and idc_directory:
        if public_ip or private_ip:
            h_path = hosts_path+'/'+idc_directory
            if not os.path.exists(h_path):
                os.makedirs(h_path)
            if os.path.exists(h_path):
                if not os.path.exists(h_path+'/'+service_directory):
                    os.makedirs(h_path+'/'+service_directory)
                if os.path.exists(h_path+'/'+service_directory):
                    path = h_path+'/'+service_directory+'/'+host_name+'.cfg'
                    if not os.path.exists(path):
                        with open(path,'w') as f:
                            for i in items:
                                f.write(i)
                    else:
                        print path,' Already exists..'
                    template_path = '/opt/ourpalm/www/nagios/etc/conf.d/Templates'
                    print template_path+'/'+idc_region+'_'+service_name+'_'+'hosttemplate.cfg'
                    if not os.path.exists(template_path+'/'+idc_region+'_'+service_name+'_'+'hosttemplate.cfg'):
                        with open(template_path+'/'+idc_region+'_'+service_name+'_'+'hosttemplate.cfg','w') as f:
                            for i in templa:
                                f.write(i)
                else:
                    print service_directory
            else:
                print idc_directory
        else:
            print public_ip,private_ip

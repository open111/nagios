#!/usr/bin/env python




import os
import sys
import time


def hostgroups(dict):
    service_name      = dict['service_name']
    service_directory = dict['service_directory']
    idc_name          = dict['idc_name']
    idc_directory     = dict['idc_directory']
    idc_region        = dict['idc_region']
    group_name        = dict['group_name']
    group_directory   = dict['group_directory']
    public_ip         = dict['public_ip']
    private_ip        = dict['private_ip']
    temp              = '/tmp/nagios/hostgroups'
    date              = time.strftime('%F-%T')
    hosts_path        = dict['Hosts']
    hostgroups_path   = dict['Hostgroups']
    services_path     = dict['Services']


    if service_name and group_name and group_directory:
        if public_ip or private_ip:
            if os.path.exists(group_directory):
                if os.path.exists(group_directory+'/'+group_name):
                    contents = []
                    if public_ip:
                        host_name = idc_region+'_'+service_name+'_'+public_ip
                    else:
                        host_name = idc_region+'_'+service_name+'_'+private_ip

                    #print host_name
                    modify = False
                    with open(group_directory+'/'+group_name) as f:
                        for x in f.readlines():
                            s = x.strip()
                            if s.startswith('members'):
                                l = s.split()[0]
                                r = s.split()[1].strip('\n')
                                r = r.split(',')
                                if host_name in r:
                                    contents.append(x)
                                else:
                                    modify = True
                                    r.append(host_name)
                                    r = ','.join(r)
                                    contents.append('\tmembers \t%s\n' %r)
                            else:
                                contents.append(x)

                    if modify:
                        if os.path.exists(temp):
                            open(temp+'/'+group_name+'_'+date,'wb').write(open(group_directory+'/'+group_name,'rb').read())
                            #for i in contents:
                            #    print i,
                            with open(group_directory+'/'+group_name,'w') as f:
                                for i in contents:
                                    f.write(i)
                        else:
                            print temp,' Not Found...'
                            return (-1,'Not Found...')
                        
                                



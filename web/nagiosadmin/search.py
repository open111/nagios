#!/usr/bin/env python


import os
import sys


def search(dict):
    host_name          = dict['host_name']
    service_name       = dict['service_name']
    service_directory  = dict['service_directory']
    idc_name           = dict['idc_name']
    idc_directory      = dict['idc_directory']
    idc_region         = dict['idc_region']
    group_name         = dict['group_name']
    group_directory    = dict['group_directory']
    hosts_path         = dict['Hosts']
    hostgroups_path    = dict['Hostgroups']
    services_path      = dict['Services']

    cpu       = dict['CPU']
    memory    = dict['MEMORY']
    storage   = dict['STORAGE']
    temp      = dict['TEMP']
    power     = dict['POWER']
    other     = dict['OTHER']

    if host_name and service_name and service_directory and idc_name \
        and idc_region and group_name and group_directory and idc_directory \
        and services_path and hostgroups_path and hosts_path:
            h_path = hosts_path      +'/' +idc_directory   +'/'+service_directory
            s_path = services_path   +'/' +idc_directory   +'/'+service_directory
            g_path = group_directory

            files = {'cpu'         : [s_path+'/'+'cpu'       +'/' + host_name+'_cpu.cfg',False],
                     'memory'      : [s_path+'/'+'memory'    +'/' + host_name+'_memory.cfg',False],
                     'load'        : [s_path+'/'+'load'      +'/' + host_name+'_load.cfg',False],
                     'disk_root'   : [s_path+'/'+'disk_root' +'/' + host_name+'_disk_root.cfg',False],
                     'disk_opt'    : [s_path+'/'+'disk_opt'  +'/' + host_name+'_disk_opt.cfg',False],
                     'hosts'       : [h_path+'/'+ host_name  + '.cfg',False],
                     'hostgroups'  : [g_path+'/'+ group_name,False],
                     'omsa_cpu'    : [cpu,False],
                     'omsa_memory' : [memory,False],
                     'omsa_storage': [storage,False],
                     'omsa_temp'   : [temp,False],
                     'omsa_power'  : [power,False],
                     'omsa_other'  : [other,False]} 


            for k,v in files.items():
                if os.path.exists(v[0]):
                    if k == 'hostgroups':
                        with open(v[0]) as f:
                            for x in f.readlines():
                                s = x.strip()
                                if s.startswith('members'):
                                    l = s.split()[0]
                                    r = s.split()[1].strip('\n')
                                    r = r.split(',')
                                    if host_name in r:
                                        files[k][1] = True
                    elif k.startswith('omsa_'):
                        with open(v[0]) as f:
                            for x in f.readlines():
                                s = x.strip()
                                if s.startswith('host_name'):
                                    l = s.split()[0]
                                    r = s.split()[1].strip('\n')
                                    r = r.split(',')
                                    if host_name in r:
                                        files[k][1] = True
                    else:
                        files[k][1] = True

            return files



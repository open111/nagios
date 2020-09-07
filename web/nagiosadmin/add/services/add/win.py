#!/usr/bin/env python

import os
import sys


def win(dict):
    service_name = dict['service_name']
    service_directory = dict['service_directory']
    idc_name = dict['idc_name']
    idc_directory = dict['idc_directory']
    idc_region = dict['idc_region']
    public_ip = dict['public_ip']
    private_ip = dict['private_ip']
    hosts_path = dict['Hosts']
    hostgroups_path = dict['Hostgroups']
    services_path = dict['Services']

    if public_ip or private_ip and service_name and service_directory \
            and idc_name and idc_directory and idc_region and services_path:

        if public_ip or private_ip:
            if public_ip:
                host_name = idc_region + '_' + service_name + '_' + public_ip
            else:
                host_name = idc_region + '_' + service_name + '_' + private_ip
            print idc_region

            service = {'check_alldisk': {'directory': 'check_alldisk', 'disk': '/'},
                       'memory': {'directory': 'memory', 'memory': '-W 90 -C 95 -A memused'},
                       'load': {'directory': 'load', 'load': '5,80,90'}}

            for k, v in service.items():
                if v.has_key('memory'):
                    m1 = ['define service{\n',
                          '\thost_name           %s\n' % (host_name),
                          '\tservice_description check_memused\n',
                          '\tdisplay_name        check_memused\n',
                          '\tuse                 ops_service_p2\n',
                          '\tcheck_command       check_nt!MEMUSE!"-w 80 -c 90"\n',
                          '\tregister            1\n',
                          '}\n']
                    items = [m1]

                if v.has_key('disk'):
                    d1 = ['define service{\n',
                          '\thost_name           %s\n' % (host_name),
                          '\tservice_description %s\n' % (service_name + '_' + k),
                          '\tdisplay_name        %s\n' % (service_name + '_' + k),
                          '\tuse                 %s\n' % (idc_region + '_' + service_name + '_ops_service_p1'),
                          # '\tcheck_command       check_nrpe!check_disk!"-w 10% -c 5% -u GB -p '+ v['disk'] + '"\n',
                          '\tcheck_command	     check_nt!USEDDISKSPACE!c!"-w 90 -c 95"\n'
                          '\tregister            1\n',
                          '}\n']
                    items = [d1]

                if v.has_key('load'):
                    l1 = ['define service{\n',
                          '\thost_name           %s\n' % (host_name),
                          '\tservice_description %s\n' % (k),
                          '\tdisplay_name        %s\n' % (k),
                          '\tuse                 %s\n' % (idc_region + '_' + service_name + '_ops_service_p2'),
                          '\tcheck_command       check_nt!CPULOAD!"' + v['load'] + '"\n',
                          '\tregister            1\n',
                          '}\n']
                    items = [l1]

                if not os.path.exists(services_path + '/' + idc_directory):
                    os.makedirs(services_path + '/' + idc_directory)

                ser_path = services_path + '/' + idc_directory + '/' + service_directory
                if not os.path.exists(ser_path):
                    os.makedirs(ser_path)
                if os.path.exists(ser_path):
                    if not os.path.exists(ser_path + '/' + v['directory']):
                        os.makedirs(ser_path + '/' + v['directory'])
                    if os.path.exists(ser_path + '/' + v['directory']):
                        f_path = ser_path + '/' + v['directory'] + '/' + host_name + '_' + k + '.cfg'
                        if not os.path.exists(f_path):
                            print f_path
                            with open(f_path, 'w') as f:
                                for i in items:
                                    for x in i:
                                        f.write(x)
                        else:
                            f_path, '  existing...'
                    else:

                        print ser_path + '/' + v['directory'], ' Not Found...'



                else:
                    print ser_path, ' Not Found...'

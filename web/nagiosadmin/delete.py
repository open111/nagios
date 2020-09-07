#!/usr/bin/env python


import os
import sys
import commands


def batch_search(dict):
    host_name  = dict['host_name']
    Hosts      = dict['Hosts']
    Hostgroups = dict['Hostgroups']
    Services   = dict['Services']

    ststus,host_files = commands.getstatusoutput('grep -rlw %s %s' %( host_name, Hosts ))
    status,hostgroup_files = commands.getstatusoutput('grep -rlw %s %s' %( host_name, Hostgroups ))
    status,service_files = commands.getstatusoutput('grep -rlw %s %s' %( host_name, Services ))

    remove_lists = []

    if host_files:
        for i in host_files.split('\n'):
            remove_lists.append({
                    'host_name':host_name,
                    'file_name':i,
            })

    if hostgroup_files:
        for i in hostgroup_files.split('\n'):
            remove_lists.append({
                    'host_name':host_name,
                    'file_name':i,
            })

    if service_files:
        for i in service_files.split('\n'):
            remove_lists.append({
                    'host_name':host_name,
                    'file_name':i,
            })

    return remove_lists


def batch_delete(remove_lists):
    for i in remove_lists:
        contents = []
        removefile = []
        with open(i['file_name']) as f:
            for x in f:
                if i['host_name'] in x:
                    s = x.strip()
                    l = s.split()[0]
                    r = s.split()[1].strip('\n')
                    r = r.split(',')
                    r.remove(i['host_name'])
                    if len(r) == 0:
                        contents = []
                        os.remove(i['file_name'])
                        removefile.append(i['file_name'])
                        print 'remove file %s' %i['file_name']
                        break
                    r = ','.join(r)
                    contents.append('\t%s \t%s\n' %(l,r))
                else:
                    contents.append(x)
            

        if i['file_name'] not in removefile:
            with open(i['file_name'],'w') as f:
                for i in contents:
                    f.write(i)

    


def single(dict):
    for k,v in dict.items():
        contents = []
        if k == 'hostgroups':
            if v[2] == 'True':
                host_name = v[0]
                modify = False

                with open(v[1]) as f:
                    for x in f.readlines():
                        s = x.strip()
                        if s.startswith('members'):
                            l = s.split()[0]
                            r = s.split()[1].strip('\n')
                            r = r.split(',')
                            if host_name in r:
                                modify = True
                                r.remove(host_name)
                                r = ','.join(r)
                                contents.append('\tmembers \t%s\n' %r)
                                
                            else:
                                contents.append(x)
                        else:
                           contents.append(x)

                if modify:
                    with open(v[1],'w') as f:
                        for i in contents:
                            f.write(i)
  
        elif k.startswith('omsa'):
            if v[2] == 'True':
                host_name = v[0]
                modify = False

                with open(v[1]) as f:
                    for x in f.readlines():
                        s = x.strip()
                        if s.startswith('host_name'):
                            l = s.split()[0]
                            r = s.split()[1].strip('\n')
                            r = r.split(',')
                            if host_name in r:
                                modify = True
                                r.remove(host_name)
                                r = ','.join(r)
                                contents.append('\thost_name \t%s\n' %r)

                            else:
                                contents.append(x)
                        else:                                                                                              
                           contents.append(x)                                                                              
                                                                                                                           
                if modify:                                                                                                 
                    with open(v[1],'w') as f:                                                                              
                        for i in contents:                                                                                 
                            f.write(i)

        else:
            if v[2] == 'True':
                os.system('rm -f %s' %v[1])

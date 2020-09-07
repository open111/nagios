#!/usr/bin/env python


import os
import sys
import time


def omsa(dict):
    cpu       = dict['CPU']
    memory    = dict['MEMORY']
    storage   = dict['STORAGE']
    temp      = dict['TEMP']
    power     = dict['POWER']
    other     = dict['OTHER']
    host_name = dict['host_name']
    tmp       = '/tmp/nagios/services/omsa'
    date      = time.strftime('%F-%T')

    if not os.path.exists(tmp):
        os.system('mkdir -p %s' %tmp)

    files = {'cpu'     :cpu,
             'memory'  :memory,
             'storage' :storage,
             'temp'    :temp,
             'power'   :power,
             'other'   :other,}

    for k,v in files.items():
        contents = []
        Modify = False
        with open(v) as f:
            for x in f.readlines():
                s = x.strip()
                if s.startswith('host_name'):
                    l = s.split()[0]
                    r = s.split()[1].strip('\n')
                    r = r.split(',')
                    if host_name in r:
                        Modify = False
                        contents.append(x)
                    else:
                        r.append(host_name)
                        r = ','.join(r)
                        contents.append('\thost_name \t%s\n' %r)
                        Modify = True
                else:
                    contents.append(x)
            
            if Modify:
                open(tmp+'/'+k+'_'+date,'wb').write(open(v).read())
                with open(v,'w') as f:
                    for i in contents:
                        f.write(i)

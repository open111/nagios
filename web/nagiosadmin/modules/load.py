#!/usr/bin/env python
#coding:utf-8

import nagios
import query
import auth

def LoadNagios():
    n = nagios.Nagios()
    nagios_data = n.update()
    return nagios_data

def LoadSql(action):
    if action == 'status_1':
        data = query.status_1()
        return data
    if action == 'status_0':
        data = query.status_0()
        return data

def LoadHost(ip):
    data = query.query_host(ip)
    return data


def load():
    nagios_data = LoadNagios()['Hosts']
    status_1 = LoadSql('status_1')
    ip_lists = []
    no_monitor = []
    for k,v in nagios_data.items():
        for ip in v['define host']['address']:
            ip = ip.strip()
            if ip not in ip_lists:
                ip_lists.append(ip)
    for line in status_1:
        pub = line[1].strip()
        if pub == '113.31.131.210':
            print line
        pri = line[2].strip()
        if pub not in ip_lists and pri not in ip_lists:
            no_monitor.append(line)
    if no_monitor:
        return no_monitor
    else:
        return {}



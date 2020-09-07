#!/usr/bin/env python

import os
import sys
from modules import load
from logger_C import Logger

currPath = os.path.split(os.path.realpath(__file__))[0]
log_filename = currPath + "/nagiosadmin.log"
logger = Logger(logname=log_filename, loglevel=1, logger="wn", output=1).getlog()


def hosts(dict):
    for k in dict:
        if dict[k]['type'] == 'host' and dict[k]['os'] == 'OSlinux':
            #print dict[k]['os']
            from add.hosts.add import hosts
            from add.hostgroups.add import hostgroups
            from add.services.add.bases import bases
            h = hosts(dict[k])
            g = hostgroups(dict[k])
            s = bases(dict[k])
        else:
            from add.hosts.add import hosts
            from add.hostgroups.add import hostgroups
            from add.services.add.win import win
            h = hosts(dict[k])
            g = hostgroups(dict[k])
            s = win(dict[k])



def omsa(dict):
    from add.services.add.omsa import omsa
    o = omsa(dict)

def mysql(dict):
    from add.services.add.mysql import mysql
    m = mysql(dict)


def mongo(dict):
    from add.services.add.mongo import mongo
    m = mongo(dict)

def redis(dict):
    from add.services.add.redis import redis
    m = redis(dict)


def tcp(dict):
    from add.services.add.tcp import tcp
    m = tcp(dict)


def _search(dict):
    from search import search
    s = search(dict)
    return s
    

def batch_search(dict):
    from delete import batch_search
    s = batch_search(dict)
    return s


def batch_delete(list):
    from delete import batch_delete
    d = batch_delete(list)
    return d


def single_delete(dict):
    from delete import single
    d = single(dict)


def Search(ip):
    dict = {}
    data = load.LoadNagios()
    #logger.debug("data:%s" % data)
    hosts = data['Hosts']
    services = data['Services']
    hostgroups = data['Hostgroups']
    for k,v in hosts.items():
        if v['define host']['address'].count(ip):
            dict['Hosts'] = hosts[k]
	    #print "dict['Hosts']:%s" % dict['Hosts']
            for k1,v1 in services.items():
               if k1 == k:
		 # dict['Services'] =v['define service']['service_description']
	           dict['Services'] = services[k]
	#	   print dict['Services']
	    #dict['Services'] = services[k]
	    #print services.items()
	    #print dict['Services']
            #return dict
	    #print "dict1:%s" % dict
            for k1,v in hostgroups.items():
               if v['define hostgroup']['members'].count(k):
                   dict['Hostgroups'] = v['define hostgroup']['hostgroup_name']
		#   print "dict2:%s" % dict
            return dict
            #if i['define hostgroup']['members'].count(k):
            #    dict['Hostgroups'] = i
            #    return dict

def Templates():
    dict = {}
    data = load.LoadNagios()
    templates = data['Templates']
    contacts = data['Contacts']
    for k,v in templates.items():
        if not dict.has_key(k):
            dict[k] = {}
        if templates[k].has_key('service_description'):
            dict[k]['service_description'] = v['service_description']
        elif templates[k].has_key('alias'):
            dict[k]['service_description'] = v['alias']
        if templates[k].has_key('contact_groups'):
            dict[k]['contact_groups'] = v['contact_groups']

    for k,v in dict.items():
        if v.has_key('contact_groups'):
            if contacts.has_key(v['contact_groups']):
                dict[k]['contacts'] = contacts[v['contact_groups']]['members']
        
    for k,v in dict.items():
        if not dict[k]:
            del dict[k]
    return dict

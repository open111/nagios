#/usr/bin/env python

import os
import sys
from ConfigParser import ConfigParser
from nagiosadmin.logger_C import Logger
config = ConfigParser()
config.read('/usr/lib/python2.6/site-packages/nagios/MonitorManager/nagios/web/nagiosadmin/modules/nagios.ini')

currPath = os.path.split(os.path.realpath(__file__))[0]
log_filename = currPath + "/modules-nagios.log"
logger = Logger(logname=log_filename, loglevel=1, logger="wn", output=1).getlog()


class Nagios:

    def __init__(self):
        self.hosts = {}
        self.services = {}
        self.hostgroups = {}
        self.templates = {}
        self.contacts = {}
        self.dict = {}

    def Readfile(self,fileName):
        #print fileName
        with open(fileName) as f:
            data = f.readlines()
        return (data)

    def Handle(self,name,data):
        if name == 'hosts':
            self.Hosts(data)
        elif name == 'hostgroups':
            self.HostGroups(data)
        elif name == 'services':
            self.Services(data)
        elif name == 'templates':
            self.Templates(data)
        elif name == 'commands':
            self.Commands(data)
        elif name == 'contacts':
            self.Contacts(data)

    def Hosts(self,data):
        #print data
        for line in data:
            line = line.strip()
	    #logger.debug("data:%s" % data)
            if line.startswith('host_name'):
                #print line
                host_name = line.split()[1]
                Pub_Ip = host_name.split('_')[-1]
		#print host_name
		#print Pub_Ip
                if not self.hosts.has_key(host_name):
                    self.hosts[host_name] = {}
		    #print self.hosts
            if line.startswith('alias'):
                alias = line.split()[1]
            
            if line.startswith('address'):
                address = line.split()[1]
                #print address

            if line.startswith('use'):
                use = line.split()[1].split(',')[0]

            if line.startswith('}'):
                self.hosts[host_name]['define host'] = {'host_name':host_name,'alias':alias,'address':[Pub_Ip,address],'use':use}
            
    def HostGroups(self,data):
        #print data
        for line in data:
            line = line.strip()
            if line.startswith('hostgroup_name'):
                hostgroup_name = line.split()[1]
            if line.startswith('alias'):
                alias = line.split()[1]
            if line.startswith('members'):
                members = line.split()[1]
            if line.startswith('}'):
                if ',' in members:
                    member_lists = members.split(',')
                    #print member_lists
                    if not self.hostgroups.has_key(hostgroup_name):
                        self.hostgroups[hostgroup_name] = {}
                        self.hostgroups[hostgroup_name]['define hostgroup'] = {'hostgroup_name':hostgroup_name,'alias':alias,'members':member_lists}
                else:
                    if not self.hostgroups.has_key(hostgroup_name):
                        self.hostgroups[hostgroup_name] = {}
                        self.hostgroups[hostgroup_name]['define hostgroup'] = {'hostgroup_name':hostgroup_name,'alias':alias,'members':members}


    def Services(self,data):
        #print data
        for line in data:
            #print line
            line = line.strip()
            if line.startswith('host_name'):
                host_name = line.split()[1]
                #print host_name

            if line.startswith('service_description'):
                service_description = line.split()[1]

            if line.startswith('display_name'):
                display_name = line.split()[1]

            if line.startswith('use'):
                use = line.split()[1]

            if line.startswith('check_command'):
                check_command = line.split()[1]

            if line.startswith('}'):
                global host_name
		if ',' in host_name:        
		    #print host_name
		    host_lists = host_name.split(',')
                    for host in host_lists:
                        if self.services.has_key(host):
                            self.services[host][service_description] = {'host_name':host,'service_description':service_description,'display_name':display_name,'use':use,'check_command':check_command}
                        else:
                            self.services[host] = {}
                            self.services[host][service_description] = {'host_name':host,'service_description':service_description,'display_name':display_name,'use':use,'check_command':check_command}
                else:
                    if self.services.has_key(host_name):
                        self.services[host_name][service_description] = {'host_name':host_name,'service_description':service_description,'display_name':display_name,'use':use,'check_command':check_command}
                    else:
                        self.services[host_name] = {}
                        self.services[host_name][service_description] = {'host_name':host_name,'service_description':service_description,'display_name':display_name,'use':use,'check_command':check_command}


    def Templates(self,data):
        for line in data:
            line = line.strip()
            l = line.split()
            if l[0] == 'define':continue
            if l[0] == '}':continue
            if l[0] == 'name':
                name = l[1]
                #print name
                if not self.templates.has_key(name):
                    self.templates[name] = {}
            #print l[0],l[1]
            self.templates[name][l[0]] = l[1]

    def Contacts(self,data):
        for line in data:
            line = line.strip()
            #print line 
            l = line.split()
            #print l[0],l[1]
            try:
                if l[0] == 'define':continue
            except IndexError:
                continue
            if l[0] == '}':continue
            if l[0] == 'contactgroup_name':
                contactgroup_name = l[1]
                #print contactgroup_name
                if not self.contacts.has_key(contactgroup_name):
                    self.contacts[contactgroup_name] = {}
            elif l[0] == 'contact_name':
                contact_name = l[1]
                if not self.contacts.has_key(contact_name):
                    self.contacts[contact_name] = {}
            try:
                self.contacts[contactgroup_name][l[0]] = l[1]
            except:
                self.contacts[contact_name][l[0]] = l[1]


    def update(self):
        for items in config.items('nagios'):
            name = items[0]
            path = items[1]
            for parent,dirnames,filenames in os.walk(path):
                for filename in filenames:
                    if os.path.splitext(filename)[-1] == '.cfg':
                        data = self.Readfile(os.path.join(parent,filename))
                        self.Handle(name,data)
        self.dict['Hosts'] = self.hosts
        self.dict['Services'] = self.services
        self.dict['Hostgroups'] = self.hostgroups
        self.dict['Templates'] = self.templates
        self.dict['Contacts'] = self.contacts
        #print self.dict['Hostgroups']
        return self.dict


if __name__ == '__main__':
    p = Nagios()
    p.update()

#!/usr/bin/env python

import __init__
import optparse


#def add(m_type,service_type,service_items):
def nagios_add(args):
    if args[0] == 'service':
        if args[1] == 'omsa':
            import nagios.add.services.omsa.omsa
            if args[2] and args[3]:
                if args[2] == 'all':
                    items = ['cpu','mem','storage','power','temp','other']
                    for i in items:
                        nagios.add.services.omsa.omsa.add(i,args[3])
                else:
                    nagios.add.services.omsa.omsa.add(args[2],args[3])
            


def nagios_delete(args):
    if args[0] == 'service':
        if args[1] == 'omsa':
            import nagios.delete.services.omsa.omsa
            if args[2] and args[3]:
                if args[2] == 'all':
                    items = ['cpu','mem','storage','power','temp','other']
                    for i in items:
                        nagios.delete.services.omsa.omsa.delete(i,args[3])
                else:
                    nagios.delete.services.omsa.omsa.delete(args[2],args[3])


#add('services','omsa','cpu')

if __name__ == '__main__':
    parser = optparse.OptionParser(usage="usage: %prog [options]",description="Nagios Query API..")
    parser.add_option("-a", "--add",help="Input Server IP Query..")
    parser.add_option("-d", "--delete",help="Input Server IP Query..")
    opts, args = parser.parse_args()
    print opts,args
    if opts.add:
        if opts.add == 'add':
            nagios_add(args)

    if opts.delete:
        if opts.delete == 'del':
            nagios_delete(args)

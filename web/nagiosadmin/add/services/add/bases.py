#!/usr/bin/env python

import os
import sys



def bases(dict):
    service_name      = dict['service_name']
    service_directory = dict['service_directory']
    idc_name          = dict['idc_name']
    idc_directory     = dict['idc_directory']
    idc_region        = dict['idc_region']
    public_ip         = dict['public_ip']
    private_ip        = dict['private_ip']
    hosts_path        = dict['Hosts']
    hostgroups_path   = dict['Hostgroups']
    services_path     = dict['Services']

    if public_ip or private_ip and service_name and service_directory \
       and idc_name and idc_directory and idc_region and services_path:
        
        if public_ip or private_ip:
            if public_ip:
                host_name = idc_region+'_'+service_name+'_'+public_ip
            else:
                host_name = idc_region+'_'+service_name+'_'+private_ip
	    print idc_region

            if idc_region == 'BJYZ_HLGW' or idc_region == 'BJCC_KDDI':

               ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H ntp.d.zqdaemon.com -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']
		 

	    elif idc_region == 'krkinx':
	       ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H krntp.d.zqdaemon.com -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']
            elif idc_region == 'Twcht':
               ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H 10.51.1.121 -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']
            elif idc_region == 'hkntt':
               ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H hkntp.d.zqdaemon.com -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']
	    elif idc_region == 'Aws_SG':
               ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H awssgntp.d.zqdaemon.com -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']
	    elif idc_region == 'Aws_JP':
               ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H awsjpntp.d.zqdaemon.com -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']
	    elif idc_region == 'ALY_SG':
               ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H alysgntp.d.zqdaemon.com -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']
	    elif idc_region == 'VNM_VTN':
               ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H 192.168.129.72 -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']
            elif idc_region == 'ALY_USAVA':
               ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H alyusvantp.d.zqdaemon.com -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']

            elif idc_region == 'BJ_ZhongJingYun':
               ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H ntp-zjy.d.zqdaemon.com -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']

            elif idc_region == 'TM_TXBJ3':
               ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H 10.18.0.6 -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']

            elif idc_region == 'TX_TJQY':
               ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H 10.19.0.17 -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']

            elif idc_region == 'TM_TXGZ4':
               ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H 10.61.0.90 -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']

            elif idc_region == 'KSCN_TM':
               ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H 10.90.0.81 -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']

            elif idc_region == 'Zenlayer_HK2':
               ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H 10.201.4.7 -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']

            elif idc_region == 'ZL_SGSG':
               ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H sgeq.d.zqdaemon.com -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']

            elif idc_region == 'TX_SGSG':
               ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H sgeq.d.zqdaemon.com -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']

            elif idc_region == 'TM_TXBJ5':
               ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H tmtxbj5ntp.d.zqdaemon.com -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']

            else:
	       ntp = ['define service{\n',
                      '\thost_name           %s\n' %(host_name),
                      '\tservice_description check_ntp_time\n',
                      '\tdisplay_name        check_ntp_time\n',
                      '\tuse                 ops_service_ntp_p3\n',
                      '\tcheck_command       check_nrpe!check_ntp_time!"-H cn.pool.ntp.org -w 0.5 -c 1"\n',
                      '\tregister            1\n',
                      '}\n']

#            if idc_region == 'BJZW' or idc_region == 'BJCC_KDDI':
#               snoopy = ['define service{\n',
#                      '\thost_name           %s\n' %(host_name),
#                      '\tservice_description check_snoopy\n',
#                      '\tdisplay_name        check_snoopy\n',
#                      '\tuse                 ops_service_snoopy_p1\n',
#                      '\tcheck_command       check_snoopy\n',
#                      '\tregister            1\n',
#                      '}\n']
#	    else:
	    #   snoopy = []

            service = {'check_alldisk':{'directory':'check_alldisk','disk':'/'},
                       #'disk_opt' :{'directory':'disk_opt' ,'disk':'/opt'},
                       'snoopy'   :{'directory':'snoopy'   ,'snoopy':''},
                       'cpu'      :{'directory':'cpu'      ,'cpu':'-w 70 -c 90'},
                       'memory'   :{'directory':'memory'      ,'memory':'-W 90 -C 95 -A memused'},
        #               'init'      :{'directory':'init'      ,'init':''},
	#	       'ntp_time' :{'directory':'ntp_time' ,'ntp_time':'-H ntp.d.zqdaemon.com -w 0.5 -c 1'},
                       'load'     :{'directory':'load'     ,'load':'30,25,20'}}

            for k,v in service.items():
                if v.has_key('memory'):
                    m1  = ['define service{\n',
                             '\thost_name           %s\n' %(host_name),
                             '\tservice_description check_linux_status_memused\n',
                             '\tdisplay_name        check_linux_status_memused\n',
                             '\tuse                 ops_service_p2\n',
                             '\tcheck_command       check_linux_status_memused!"-W 90 -C 95 -A memused"\n',
                             '\tregister            1\n',
                             '}\n']
                    items = [m1]
                if v.has_key('disk'):
                    d1  = ['define service{\n',
                             '\thost_name           %s\n' %(host_name),
                             '\tservice_description %s\n' %(service_name+'_'+k),
                             '\tdisplay_name        %s\n' %(service_name+'_'+k),
                             '\tuse                 %s\n' %(idc_region+'_'+service_name+'_ops_service_p1'),
                             #'\tcheck_command       check_nrpe!check_disk!"-w 10% -c 5% -u GB -p '+ v['disk'] + '"\n',                             
			     '\tcheck_command	    check_alldisk!check_alldisk!"90 95"\n'
			     '\tregister            1\n',
                             '}\n']
                    items = [d1]
                if v.has_key('snoopy'):
		    s1  = ['define service{\n',
                	     '\thost_name           %s\n' %(host_name),
                      	     '\tservice_description check_snoopy\n',
                      	     '\tdisplay_name        check_snoopy\n',
                      	     '\tuse                 ops_service_snoopy_p1\n',
                      	     '\tcheck_command       check_snoopy\n',
                      	     '\tregister            1\n',
                      	     '}\n']
		    items = [s1]
                #if v.has_key('init'):
		#    i1  = ['define service{\n',
               # 	     '\thost_name           %s\n' %(host_name),
               #       	     '\tservice_description check_init\n',
               #       	     '\tdisplay_name        check_init\n',
               #       	     '\tuse                 ops_service_init_p1\n',
               #       	     '\tcheck_command       check_init\n',
               #       	     '\tregister            1\n',
               #       	     '}\n']
	       #	    items = [i1]
                if v.has_key('load'):
                    l1 = ['define service{\n',
                            '\thost_name           %s\n' %(host_name),
                            '\tservice_description %s\n' %(k),
                            '\tdisplay_name        %s\n' %(k),
                            '\tuse                 %s\n' %(idc_region+'_'+service_name+'_ops_service_p2'),
                            '\tcheck_command       check_nrpe!check_load!"-w 20,15,10 -c '+ v['load'] + '"\n',
                            '\tregister            1\n',
                            '}\n']

                    l2 = ['define service{\n',                                                                          
                            '\thost_name           %s\n' %(host_name),
                            '\tservice_description %s_night\n' %(k),
                            '\tdisplay_name        %s_night\n' %(k),
                            '\tuse                 %s\n' %(idc_region+'_'+service_name+'_ops_service_p2_night'),
                            '\tcheck_command       check_nrpe!check_load!"-w 20,15,10 -c '+ v['load'] + '"\n',
                            '\tregister            1\n',
                            '}\n']
                    items = [l1,l2]


                if v.has_key('cpu'):
                    c1 = ['define service{\n',
                            '\thost_name           %s\n' %(host_name),
                            '\tservice_description %s\n' %(k),
                            '\tdisplay_name        %s\n' %(k),
                            '\tuse                 %s\n' %(idc_region+'_'+service_name+'_ops_service_p2'),
                            '\tcheck_command       check_nrpe!check_cpu!"'+ v['cpu'] + '"\n',
                            '\tregister            1\n',
                            '}\n']


                    c2 = ['define service{\n',
                          '\thost_name           %s\n' %(host_name),
                          '\tservice_description %s_night\n' %(k),
                          '\tdisplay_name        %s_night\n' %(k),
                          '\tuse                 %s\n' %(idc_region+'_'+service_name+'_ops_service_p2_night'),
                          '\tcheck_command       check_nrpe!check_cpu!"'+ v['cpu'] + '"\n',
                          '\tregister            1\n',
                          '}\n']
		    items = [c1,c2]
		

#		if v.has_key('ntp_time'):
#                if idc_region == 'BJZW':
#                    ntp = ['define service{\n',
#                                '\thost_name           %s\n' %(host_name),
#                                '\tservice_description ntp_time\n',
#                                '\tdisplay_name        ntp_time\n',
#                                '\tuse                 ops_service_p1\n',
#                                '\tcheck_command       check_nrpe!check_ntp_time!"-H ntp.d.zqdaemon.com -w 0.5 -c 1"\n',
#                                '\tregister            1\n',
#                                '}\n']
#	           items = [ntp]	

                if not os.path.exists(services_path+'/'+idc_directory):
                    os.makedirs(services_path+'/'+idc_directory)

                ser_path = services_path+'/'+idc_directory+'/'+service_directory
                if not os.path.exists(ser_path):
                    os.makedirs(ser_path)
                if os.path.exists(ser_path):
                    if not os.path.exists(ser_path+'/'+v['directory']):
                        os.makedirs(ser_path+'/'+v['directory'])
                    if os.path.exists(ser_path+'/'+v['directory']):
                        f_path = ser_path+'/'+v['directory']+'/'+host_name+'_'+k+'.cfg'
                        if not os.path.exists(f_path):
                            print f_path
                            with open(f_path,'w') as f:
                                for i in items:
                                    for x in i:
                                        f.write(x)
                        else:
                            f_path,'  existing...'

#                    if not os.path.exists(ser_path+'/'+'check_snoopy'):
#                        os.makedirs(ser_path+'/'+'check_snoopy')
#                    if os.path.exists(ser_path+'/'+'check_snoopy'):	
#                        o_path = ser_path+'/'+'check_snoopy'+'/'+host_name+'_'+'check_snoopy'+'.cfg'
#                        if not os.path.exists(o_path):
#                            with open(o_path,'w') as f:
#                                for x in spy:
#                                        f.write(x)
#                        else:
#                            o_path,' existing...'
#                    else:
#
#                        print ser_path+'/'+'snoopy',' Not Found...'


                    if not os.path.exists(ser_path+'/'+'ntp_time'):
                        os.makedirs(ser_path+'/'+'ntp_time')
		    if os.path.exists(ser_path+'/'+'ntp_time'):	
                        n_path = ser_path+'/'+'ntp_time'+'/'+host_name+'_'+'ntp_time'+'.cfg'
                    	if not os.path.exists(n_path):
                            with open(n_path,'w') as f:
                                for i in ntp:
                                	f.write(i)
                    	else:
                            n_path,' existing...'
                    else:

                        print ser_path+'/'+v['directory'],' Not Found...'


        
                else:
                    print ser_path,' Not Found...'

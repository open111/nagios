#!/usr/bin/env python
#coding:utf8

import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from nagiosadmin.modules import load
from nagiosadmin import nagiosadmin
from web.models import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from nagiosadmin.logger_C import Logger

currPath = os.path.split(os.path.realpath(__file__))[0]
log_filename = currPath + "/log/view.log"
logger = Logger(logname=log_filename, loglevel=1, logger="wn", output=1).getlog()

def login(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,password=password)
            if user:
                auth.login(request,user)
                return HttpResponseRedirect('/')
            else:
                login_error = 'login error.'
                return render_to_response('registration/login.html', {'login_error' : login_error, 'is_display' : 'display:block'})
        return render_to_response('registration/login.html', {'is_display' : 'display:none'})

@login_required
def index(request):
    #print request
    return render_to_response('index.html')

@login_required
def search(request):
    dict = {}
    if request.method == "POST":
        ip = request.POST['search']
        if len(ip.split('.')) == 4:
            dict = nagiosadmin.Search(ip)
            return render_to_response('search.html',{'dict':dict})
    return HttpResponse('error')

@login_required
def addhosts(request):
    user = request.user
    #print request
    if request.method == "POST":

        dict = {}
        idc_id = request.POST['idc']
        service_id = request.POST['service']
        group_id = request.POST['group']
        hardware = request.POST['hardware']
        system_Os = request.POST['os']

        # if system_Os == 'OSlinux':
        if idc_id and service_id and group_id:
            idc = IDC.objects.get(id=idc_id)
            service = SERVICE.objects.get(id=service_id)
            group = HOSTGROUPS.objects.get(id=group_id)
            nagios = NAGIOS_PATH.objects.all()
            if idc and service and group:
                for k in request.POST:
                    if k in ['hardware', 'group', 'idc', 'service', 'os']: continue
                    # if k.startswith(u'ZQ') or k.startswith(u'RENT') or k.startswith(u'VNM'):
                    if True:
                        host = TEMP.objects.get(asset_no=k)
                        dict[k] = {'service_name'       :service.service_description,
                                    'service_directory'  :service.service_directory,
                                    'idc_name'           :idc.idc_description,
                                    'idc_directory'      :idc.idc_directory,
                                    'idc_region'         :idc.idc_region,
                                    'group_name'         :group.group_description,
                                    'group_directory'    :group.group_directory,
                                    'public_ip'          :host.public_ip,
                                    'private_ip'         :host.private_ip,
                                    'type'               :'host',
                                    'os'                 :system_Os,}

                        for i in nagios:
                            dict[k][i.name] = i.directory

                        if hardware == 'yes':
                            if host.public_ip and host.private_ip:
                                host_name = idc.idc_region+'_'+service.service_description+'_'+host.public_ip
                            elif host.public_ip:
                                host_name = idc.idc_region+'_'+service.service_description+'_'+host.public_ip
                            else:
                                host_name = idc.idc_region+'_'+service.service_description+'_'+host.private_ip
                            d = OMSA.objects.all()
                            hardwa = {}
                            hardwa['host_name'] = host_name
                            for i in d:
                                hardwa[i.service_name] = i.service_directory
                            o = nagiosadmin.omsa(hardwa)

                        r = nagiosadmin.hosts(dict)
                        OPERATOR_LOG.objects.create(oper_user=user,
                                                    oper_log='%s %s %s %s' %(k,dict[k]['public_ip'],dict[k]['private_ip'],dict[k]['service_name']),
                                                    oper_service='Hosts',
                                                    oper_type='Add')
        else:
            return HttpResponse('error')
                
    data = load.load()
    TEMP.objects.all().delete()
    for i in data:
        asset_no = i[0].strip()
        public_ip = i[1].strip()
        if public_ip == '无' or len(public_ip.split('.')) != 4:
            public_ip = ''
        private_ip = i[2].strip()
        if private_ip == '无' or len(private_ip.split('.')) != 4:
            private_ip = ''
        try:
            idc_name = i[3].strip()
        except:
            idc_name = ''
    
        try:
            service_name = i[4].strip()
        except:
            service_name = ''

        try:
            use_dept_name = i[6].strip()
        except:
            use_dept_name = ''

        try:
            ostype = i[10].strip()
        except:
            ostype = ''

        TEMP.objects.create(asset_no = asset_no,
                           public_ip = public_ip,
                           private_ip = private_ip,
                           idc_name = idc_name,
                           service_name = service_name,
                           use_dept_name = use_dept_name,
                           ostype = ostype,)

    data = TEMP.objects.all()
    idc = IDC.objects.all()
    service = SERVICE.objects.all()
    group = HOSTGROUPS.objects.all()
    return render_to_response('add/hosts.html',{ 'data':data, 'idc':idc, 'service':service, 'group':group })


@login_required
def addmysql(request):
    user = request.user
    Templates.objects.all().delete()
    data = nagiosadmin.Templates()
    for k,v in data.items():
        contacts_groups = ''
        if v.has_key('contacts_groups'):
            contacts_groups = v['contacts_groups']
        contacts = ''
        if v.has_key('contacts'):
            contacts = v['contacts']
        Templates.objects.create(temp_name=v['service_description'],
                                 temp_description=k,
                                 temp_contacts=contacts,
                                 temp_contact_groups=contacts_groups)
    if request.method == 'POST':
        m_type = request.POST['m_type']
        ip = request.POST['ip']
        template = request.POST['templates']
        s = request.POST['service']
        idc = request.POST['idc']
        port = request.POST['port']
        ports = []
        if len(ip.split('.')) == 4:
            data = nagiosadmin.Search(ip)
            if data.has_key('Hosts'):
                host_name = data['Hosts']['define host']['host_name']
            else:
                return HttpResponse('error')

        for i in port.split(','):
            if i.count('-'):
                a,b = i.split('-')
                for x in range(int(a),int(b)+1):
                    ports.append(str(x))
            else:
                ports.append(i)
        if m_type and ip and template and s and idc and ports:
            service = SERVICE.objects.get(id=s)
            idc = IDC.objects.get(id=idc)
            nagios = NAGIOS_PATH.objects.all()
            dict = {'service_name'       :service.service_description,
                    'service_directory'  :service.service_directory,
                    'idc_name'           :idc.idc_description,
                    'idc_directory'      :idc.idc_directory,
                    'idc_region'         :idc.idc_region,
                    'template'           :template,
                    'host_name'          :host_name,
                    'private_ip'         :ip,
                    'ports'              :ports,
                    'm_type'             :m_type,}
                                    
            for i in nagios:
                    dict[i.name] = i.directory
            nagiosadmin.mysql(dict)
            OPERATOR_LOG.objects.create(oper_user=user,
                                        oper_log='%s %s %s' %(dict['host_name'],dict['private_ip'],dict['service_name']),
                                        oper_service='Mysql',
                                        oper_type='Add')

        else:
            return HttpResponse('error')

        
        
    idc = IDC.objects.all()
    service = SERVICE.objects.all()
    templates = Templates.objects.filter(temp_name__contains='mysql')
    return render_to_response('add/mysql.html',{'templates':templates,'idc':idc, 'service':service})


@login_required
def addmongo(request):
    user = request.user
    Templates.objects.all().delete()
    data = nagiosadmin.Templates()
    for k,v in data.items():
        contacts_groups = ''
        if v.has_key('contacts_groups'):
            contacts_groups = v['contacts_groups']
        contacts = ''
        if v.has_key('contacts'):
            contacts = v['contacts']
        Templates.objects.create(temp_name=v['service_description'],
                                 temp_description=k,
                                 temp_contacts=contacts,
                                 temp_contact_groups=contacts_groups)
    if request.method == 'POST':
        m_type = request.POST['m_type']
        ip = request.POST['ip']
        template = request.POST['templates']
        s = request.POST['service']
        idc = request.POST['idc']
        port = request.POST['port']
        ports = []
        if len(ip.split('.')) == 4:
            data = nagiosadmin.Search(ip)
            if data.has_key('Hosts'):
                host_name = data['Hosts']['define host']['host_name']
            else:
                return HttpResponse('error')

        for i in port.split(','):
            if i.count('-'):
                a,b = i.split('-')
                for x in range(int(a),int(b)+1):
                    ports.append(str(x))
            else:
                ports.append(i)
        if m_type and ip and template and s and idc and ports:
            service = SERVICE.objects.get(id=s)
            idc = IDC.objects.get(id=idc)
            nagios = NAGIOS_PATH.objects.all()
            dict = {'service_name'       :service.service_description,
                    'service_directory'  :service.service_directory,
                    'idc_name'           :idc.idc_description,
                    'idc_directory'      :idc.idc_directory,
                    'idc_region'         :idc.idc_region,
                    'template'           :template,
                    'host_name'          :host_name,
                    'private_ip'         :ip,
                    'ports'              :ports,
                    'm_type'             :m_type,}
                                    
            for i in nagios:
                    dict[i.name] = i.directory
            nagiosadmin.mongo(dict)
            OPERATOR_LOG.objects.create(oper_user=user,
                                        oper_log='%s %s %s' %(dict['host_name'],dict['private_ip'],dict['service_name']),
                                        oper_service='Mysql',
                                        oper_type='Add')

        else:
            return HttpResponse('error')

        
        
    idc = IDC.objects.all()
    service = SERVICE.objects.all()
    templates = Templates.objects.filter(temp_name__contains='mongo')
    return render_to_response('add/mongo.html',{'templates':templates,'idc':idc, 'service':service})

@login_required
def addredis(request):
    user = request.user
    Templates.objects.all().delete()
    data = nagiosadmin.Templates()
    for k,v in data.items():
        contacts_groups = ''
        if v.has_key('contacts_groups'):
            contacts_groups = v['contacts_groups']
        contacts = ''
        if v.has_key('contacts'):
            contacts = v['contacts']
        Templates.objects.create(temp_name=v['service_description'],
                                 temp_description=k,
                                 temp_contacts=contacts,
                                 temp_contact_groups=contacts_groups)
    if request.method == 'POST':
        m_type = request.POST['m_type']
        ip = request.POST['ip']
        template = request.POST['templates']
        s = request.POST['service']
        idc = request.POST['idc']
        port = request.POST['port']
        ports = []
        if len(ip.split('.')) == 4:
            data = nagiosadmin.Search(ip)
            if data.has_key('Hosts'):
                host_name = data['Hosts']['define host']['host_name']
            else:
                return HttpResponse('error')
        else:
            return HttpResponse('error')

        for i in port.split(','):
            if i.count('-'):
                a,b = i.split('-')
                for x in range(int(a),int(b)+1):
                    ports.append(str(x))
            else:
                ports.append(i)
        if m_type and ip and template and s and idc and ports:
            service = SERVICE.objects.get(id=s)
            idc = IDC.objects.get(id=idc)
            nagios = NAGIOS_PATH.objects.all()
            dict = {'service_name'       :service.service_description,
                    'service_directory'  :service.service_directory,
                    'idc_name'           :idc.idc_description,
                    'idc_directory'      :idc.idc_directory,
                    'idc_region'         :idc.idc_region,
                    'template'           :template,
                    'host_name'          :host_name,
                    'private_ip'         :ip,
                    'ports'              :ports,
                    'm_type'             :m_type,}
                                    
            for i in nagios:
                    dict[i.name] = i.directory
            nagiosadmin.redis(dict)

            OPERATOR_LOG.objects.create(oper_user=user,
                                        oper_log='%s %s %s' %(dict['host_name'],dict['private_ip'],dict['service_name']),
                                        oper_service='Redis',
                                        oper_type='Add')

        else:
            return HttpResponse('error')


    idc = IDC.objects.all()
    service = SERVICE.objects.all()
    templates = Templates.objects.filter(temp_name__contains='redis')
    return render_to_response('add/redis.html',{'templates':templates,'idc':idc, 'service':service})


@login_required
def addtcp(request):
    user = request.user
    Templates.objects.all().delete()
    data = nagiosadmin.Templates()
    for k,v in data.items():
        contacts_groups = ''
        if v.has_key('contacts_groups'):
            contacts_groups = v['contacts_groups']
        contacts = ''
        if v.has_key('contacts'):
            contacts = v['contacts']
        Templates.objects.create(temp_name=v['service_description'],
                                 temp_description=k,
                                 temp_contacts=contacts,
                                 temp_contact_groups=contacts_groups)
    if request.method == 'POST':
        ip = request.POST['ip']
        template = request.POST['templates']
        s = request.POST['service']
        idc = request.POST['idc']
        port = request.POST['port']
        type = request.POST['type']
        ports = []
        if len(ip.split('.')) == 4:
            data = nagiosadmin.Search(ip)
            if data.has_key('Hosts'):
                host_name = data['Hosts']['define host']['host_name']
            else:
                return HttpResponse('error')
        else:
            return HttpResponse('error')

        for i in port.split(','):
            if i.count('-'):
                a,b = i.split('-')
                for x in range(int(a),int(b)+1):
                    ports.append(str(x))
            else:
                ports.append(i)
        if ip and template and s and idc and ports and type:
            service = SERVICE.objects.get(id=s)
            idc = IDC.objects.get(id=idc)
            nagios = NAGIOS_PATH.objects.all()
            dict = {'service_name'       :service.service_description,
                    'service_directory'  :service.service_directory,
                    'idc_name'           :idc.idc_description,
                    'idc_directory'      :idc.idc_directory,
                    'idc_region'         :idc.idc_region,
                    'template'           :template,
                    'host_name'          :host_name,
                    'private_ip'         :ip,
                    'type'               :type,
                    'ports'              :ports,}
                                    
            for i in nagios:
                    dict[i.name] = i.directory
            nagiosadmin.tcp(dict)
            OPERATOR_LOG.objects.create(oper_user=user,
                                        oper_log='%s %s %s' %(dict['host_name'],dict['private_ip'],dict['service_name']),
                                        oper_service='Tcp',
                                        oper_type='Add')

        else:
            return HttpResponse('error')


    idc = IDC.objects.all()
    service = SERVICE.objects.all()
    templates = Templates.objects.all()
    return render_to_response('add/tcp.html',{'templates':templates,'idc':idc, 'service':service})



@login_required
def addomsa(request):
    user = request.user
    if request.method == 'POST':
        ip = request.POST['ip']
        for i in ip.split(','):
            if len(i.split('.')) == 4:
                #sql_hosts = load.LoadHost(i)
                data = nagiosadmin.Search(i)
                if not data:
                    print 'Add Fail %s' %i
                    continue
                if data.has_key('Hosts'):
                    host_name = data['Hosts']['define host']['host_name']
                else:
                    return HttpResponse('error')
            else:
                return HttpResponse('error')
            print host_name

           # asset_no = sql_hosts[0][0].strip()
           # public_ip = sql_hosts[0][1].strip()
           # if public_ip == '无':
           #     public_ip = ''
           # private_ip = sql_hosts[0][2].strip()
           # if private_ip == '无':
           #     private_ip = ''
           # idc_name = sql_hosts[0][3].strip()
           # service_name = sql_hosts[0][4].strip()
           # use_dept_name = sql_hosts[0][6].strip()
           # ostype = sql_hosts[0][12].strip()
            d = OMSA.objects.all()
            hardwa = {}
            hardwa['host_name'] = host_name
            for x in d:
                hardwa[x.service_name] = x.service_directory
            o = nagiosadmin.omsa(hardwa)
            OPERATOR_LOG.objects.create(oper_user=user,
                                        #oper_log='%s %s %s %s' %(asset_no,public_ip,private_ip,service_name),
                                        oper_log='%s' %(host_name),
                                        oper_service='omsa',
                                        oper_type='add')
           # return render_to_response('add/omsa.html',{'result':'Successfully..'})
    return render_to_response('add/omsa.html')

@login_required
def batch_delete(request):
    user = request.user
    #logger.debug("user:%s",user)
    if request.method == 'POST': 
        print request.POST
        ips = []
        remove_lists = []
        for ip in request.POST['ip'].split('\r\n'):
            ips.append(ip)
     #   logger.debug("ips:%s",ips)
        if ips:
            for ip in ips:
                if len(ip.split('.')) == 4:
      #              logger.debug("ip:%s",ip)
                    nagios_hosts = nagiosadmin.Search(ip)
       #             logger.debug("nagios_hosts:%s",nagios_hosts)
                    if nagios_hosts:
                        if nagios_hosts.has_key('Hosts'):
                            host_name = nagios_hosts['Hosts']['define host']['host_name']
                            if host_name:
                                nagios = NAGIOS_PATH.objects.all()
                                dict = {'host_name' :host_name,}
                                for i in nagios:
                                    dict[i.name] = i.directory
                                remove_lists.extend(nagiosadmin.batch_search(dict))

            if request.POST.has_key('search'):
                Contents = ''
                for i in remove_lists:
                    Contents += i['host_name'] + '  ' + i['file_name'] + '<br>'
                return HttpResponse(json.dumps(Contents))
            else:
                nagiosadmin.batch_delete(remove_lists)
                OPERATOR_LOG.objects.create(oper_user=user,                                                                
                                            oper_log='delete all %s' %(json.dumps(ips)),  
                                            oper_service='',                                                                
                                            oper_type='delete')
            
    return render_to_response('delete/batch.html')


@login_required
def deletedata(request):
    user = request.user
    if request.method == 'POST':
        dict = {}
        delete_lists = []
        for k in request.POST:
            d = Delete.objects.get(name=k)
            if d.result == 'True':
                delete_lists.append(k)
            dict[k] = [d.host_name,d.path,d.result]
        if dict:
            r = nagiosadmin.delete(dict)
            
            for i in delete_lists:
                OPERATOR_LOG.objects.create(oper_user=user,
                                            oper_log='%s %s %s %s' %(d.asset_no,d.public_ip,d.private_ip,d.service_name),
                                            oper_service=i,
                                            oper_type='delete') 
          
    return HttpResponseRedirect('/delete')


@login_required
def log(request):
    log = OPERATOR_LOG.objects.all()
    return render_to_response('manager/log.html',{'log':log})


@login_required
def restart(request):
    import commands
    dict = {}
    if request.method == "GET":
        s,r = commands.getstatusoutput('/etc/init.d/nagios status')
        if s == 0:
            dict["status"] = r
        else:
            dict["error"] = r
        return render_to_response('manager/restart.html',{'status':dict})
    if request.method == "POST":
        action = request.POST['nagios']
        if action in ["start","reload"]:
            s,r = commands.getstatusoutput('/etc/init.d/nagios checkconfig')
            if s == 0:
                s,r = commands.getstatusoutput('/etc/init.d/nagios %s' %action)
                if s == 0:
                    dict[action] = r
            else:
                 dict["checkconfig"] = r
        return render_to_response('manager/restart.html',{'status':dict})

@login_required
def contactgroups(request):
    user = request.user
    return render_to_response('contacts/contactgroups.html')


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')


def query_api(request,type,data):
    if type and data:
        dict = {}
        if type == 'idc':
            idc = IDC.objects.all()
            for i in idc:
                dict[i.idc_name] = {'name'           :i.idc_name,
                                        'idc_description':i.idc_description,
                                        'idc_directory'  :i.idc_directory,
                                        'idc_region'     :i.idc_region}

            return HttpResponse(json.dumps(dict))

        if type == 'nagios_path':
            path = NAGIOS_PATH.objects.all()
            for p in path:
                dict[p.name] = {'name':p.description,
                            'directory':p.directory}
            return HttpResponse(json.dumps(dict))

        if type == 'hostgroups':
            hostgroups = HOSTGROUPS.objects.all()
            for h in hostgroups:
                if h.group_name == data:
                    dict[h.group_name] = {'group_name'        :h.group_name,
                                          'group_description' :h.group_description,
                                          'group_directory'   :h.group_directory}

                    return HttpResponse(json.dumps(dict))

    if type == 'service':
        services = SERVICE.objects.all()
        for s in services:
            if s.service_name == data:
                dict[s.service_name] = {'service_name'        :s.service_name,
                                        'service_description' :s.service_description,
                                        'service_directory'   :s.service_directory,}
        
                return HttpResponse(json.dumps(dict))


def add_api(request):
    if request.method == "POST":
        dict = {}
        #print request.POST
        for k in request.POST:
            if k.startswith('ZQ-'):
                key = k
                dict[k] = json.loads(request.POST[k])
        
        service_name = dict[key]['service_name']
        service_directory = dict[key]['service_directory']
        idc_name = dict[key]['idc_name']
        idc_directory = dict[key]['idc_directory']
        idc_region = dict[key]['idc_region']
        group_name =  dict[key]['group_name']
        group_directory = dict[key]['group_directory']
        public_ip = dict[key]['public_ip']
        private_ip = dict[key]['private_ip']
        Hosts = dict[key]['Hosts']
        Hostgroups = dict[key]['Hostgroups']
        Services = dict[key]['Services']
        hardware = dict[key]['hardware']

        r = nagiosadmin.add(dict)

        if hardware == 'yes':
            if public_ip and private_ip:
                host_name = idc_region+'_'+service_name+'_'+public_ip
            elif public_ip:
                host_name = idc_region+'_'+service_name+'_'+public_ip
            else:
                host_name = idc_region+'_'+service_name+'_'+private_ip
                d = OMSA.objects.all()
                hardwa = {}
                hardwa['host_name'] = host_name
                for i in d:
                    hardwa[i.service_name] = i.service_directory
                o = nagiosadmin.omsa(hardwa)

        OPERATOR_LOG.objects.create(oper_user='auto',
                                    oper_log='%s %s %s %s' %(key,dict[key]['public_ip'],dict[key]['private_ip'],dict[key]['service_name']),
                                    oper_type='Add')                                                       
        
    return HttpResponse(dict)


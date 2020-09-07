from django.db import models


class NAGIOS_PATH(models.Model):
    name = models.CharField(max_length=50)
    directory = models.CharField(max_length=100)
    description = models.CharField(max_length=50,blank=True)
    
    def __unicode__(self):
        return unicode(self.name)

class IDC(models.Model):
    idc_name = models.CharField(max_length=50)
    idc_description = models.CharField(max_length=50)
    idc_directory = models.CharField(max_length=100)
    idc_region = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.idc_name)

class SERVICE(models.Model):
    service_name = models.CharField(max_length=50)
    service_description = models.CharField(max_length=50)
    service_directory = models.CharField(max_length=100)

    def __unicode__(self):
       return unicode(self.service_name)

class OMSA(models.Model):
    service_name = models.CharField(max_length=50)
    service_description = models.CharField(max_length=50)
    service_directory = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.service_name)


class MONITOR_BASE(models.Model):
    items_name = models.CharField(max_length=50)
    items_description = models.CharField(max_length=50)
    items_directory = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.items_name)


class MONITOR_SERVICE(models.Model):
    items_name = models.CharField(max_length=50)
    items_description = models.CharField(max_length=50)
    items_directory = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.items_name)   


class HOSTGROUPS(models.Model):
    group_name = models.CharField(max_length=50)
    group_description = models.CharField(max_length=50)
    group_directory = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.group_name)


class OPERATOR_LOG(models.Model):
    oper_user = models.CharField(max_length=50)
    oper_log = models.CharField(max_length=200)
    oper_time = models.DateTimeField(auto_now=True)
    oper_service = models.CharField(max_length=100)
    oper_type = models.CharField(max_length=50)

    def __unicode__(self):
        return unicode(self.oper_user)


class TEMP(models.Model):
    asset_no = models.CharField(max_length=255,primary_key=True)
    public_ip = models.IPAddressField(blank = True)
    private_ip = models.IPAddressField(blank = True)
    idc_name = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    use_dept_name = models.CharField(max_length=255)
    ostype = models.CharField(max_length=255)


class Templates(models.Model):
    temp_name = models.CharField(max_length=50)
    temp_description = models.CharField(max_length=50)
    temp_contact_groups = models.CharField(max_length=50)
    temp_contacts = models.TextField()

    def __unicode__(self):
        return unicode(self.temp_name)

class Delete(models.Model):
    name = models.CharField(max_length=50,primary_key=True)
    host_name = models.CharField(max_length=100)
    path = models.CharField(max_length=200)
    result = models.CharField(max_length=100)
    public_ip = models.IPAddressField(blank = True)
    private_ip = models.IPAddressField(blank = True)
    idc_name = models.CharField(max_length=100)
    asset_no = models.CharField(max_length=100)
    service_name = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)

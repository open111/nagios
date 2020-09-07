from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nagios.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin', include(admin.site.urls)),
    url(r'^$', 'web.views.index'),
    url(r'^search$', 'web.views.search'),
    url(r'^add/hosts$', 'web.views.addhosts'),
    url(r'^add/mysql$', 'web.views.addmysql'),
    url(r'^add/mongo$', 'web.views.addmongo'),
    url(r'^add/redis$', 'web.views.addredis'),
    url(r'^add/omsa$', 'web.views.addomsa'),
    url(r'^add/tcp$', 'web.views.addtcp'),
    url(r'^delete/batch$', 'web.views.batch_delete'),
    url(r'^delete/data$', 'web.views.deletedata'),
    url(r'^manager/log$', 'web.views.log'),
    url(r'^manager/restart$', 'web.views.restart'),
    url(r'^manage/contactgroups$', 'web.views.contactgroups'),
    url(r'^login$', 'web.views.login'),
    url(r'^logout$', 'web.views.logout'),
    url(r'^login$', 'django.contrib.auth.views.login'), 
    url(r'^query_api/(?P<type>\w+)/(?P<data>\w+)$', 'web.views.query_api'),
    url(r'^add_api$', 'web.views.add_api'),
)

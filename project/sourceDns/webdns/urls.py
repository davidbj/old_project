from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sourceDns.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'webdns.views.views.index'),
    url(r'^busi\.html', 'webdns.views.views.busi'),
    url(r'^xls\.html', 'webdns.views.views.xls'),
    url(r'^list\.html', 'webdns.views.views.list'),
    url(r'^domain\.html', 'webdns.views.views.domain'),
    url(r'^delete\.html', 'webdns.views.views.delete'),
    url(r'^logout\.html', 'webdns.views.views.logout'),
    url(r'^check_form', 'webdns.views.views.check_form'),
)

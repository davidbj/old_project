from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webdns.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', 'bind.views.views.index'),
    url(r'^index\.html', 'bind.views.views.index'),
    url(r'^form\.html', 'bind.views.views.form'),
    url(r'^delete\.html', 'bind.views.views.delete'),
    url(r'^zone\.html', 'bind.views.views.zone'),
    url(r'^delete_zone\.html', 'bind.views.views.delete_zone'),
    url(r'^xls\.html', 'bind.views.views.xls'),
    url(r'^logout\.html', 'bind.views.views.logout'),
    url(r'^$', 'bind.views.views.index'),
)

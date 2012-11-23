from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template, redirect_to
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/?$', 'dvd.views.home', name='home'),
    url(r'^notify/(?P<dvd_id>\d+)/?$', 'dvd.views.notify', name='notify'),

    url(r'^dvdadmin/?$', 'dvd.views.admin', name='admin'),

    url(r'^dvdadmin/checkout/?$', redirect_to, {'url': '/dvdadmin/checkout/1/'}),
    url(r'^dvdadmin/checkout/1/?$', 'dvd.views.checkout_1', name='checkout_1'),
    url(r'^dvdadmin/checkout/2/?$', 'dvd.views.checkout_2', name='checkout_2'),

    url(r'^dvdadmin/checkin/user/?$', 'dvd.views.checkin_user', name='checkin_user'),
    url(r'^dvdadmin/checkin/dvd/?$', 'dvd.views.checkin_dvd', name='checkin_dvd'),

    url(r'^dvdadmin/addadmin/?$', 'dvd.views.addadmin', name='addadmin'),
    url(r'^dvdadmin/dvd/add/?$', 'dvd.views.dvd_add', name='dvdadd'),
    url(r'^dvdadmin/dvd/edit/?$', 'dvd.views.dvd_edit', name='dvdedit'),
    url(r'^dvdadmin/dvd/edit/(?P<dvd_id>\d+)/?$', 'dvd.views.dvd_edit_single', name='dvdeditsingle'),
    url(r'^dvdadmin/dvd/delete/(?P<dvd_id>\d+)/?$', 'dvd.views.dvd_delete', name='dvddelete'),

    (r'^login/?$', 'django_cas.views.login'),
    (r'^logout/?$', 'django_cas.views.logout'),

    # Admin
    url(r'^admin/?$', 'django_cas.views.login', kwargs={'next_page': '/djadmin/'}),
    (r'^djadmin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()


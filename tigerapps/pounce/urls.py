#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'pounce.views.index', name='index'),
    url(r'^courses$', 'pounce.views.courses', name='courses'),
    url(r'^subscribeEmail$', 'pounce.views.subscribeEmail', name='subscribeEmail'),
    url(r'^subscribeText$', 'pounce.views.subscribeText', name='subscribeText'),
    url(r'^reactivate/(\d+)$', 'pounce.views.reactivate', name='reactivate'),
#     url(r'^course-offerings/course_details.xml', 'pounce.views.coursedetails', name='coursedetails'),
    # url(r'^princetonpounce/', include('princetonpounce.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

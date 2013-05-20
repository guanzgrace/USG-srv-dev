from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'views.index'),
	url(r'^courses$', 'views.courses'),
	url(r'^swaprequest$', 'views.swapRequest'),
    url(r'^manage$', 'views.manage'),
    url(r'^mustOverwrite$', 'views.mustOverwrite'),
    url(r'^remove/(\d+)$', 'views.remove'),

    # Examples:
    # url(r'^$', 'sectionviews.home', name='home'),
    # url(r'^sectionswap/', include('sectionswap.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

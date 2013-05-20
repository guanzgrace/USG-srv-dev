from django.conf.urls.defaults import *
import swap

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'swap.views.index'),
	url(r'^courses$', 'swap.views.courses'),
	url(r'^swaprequest$', 'swap.views.swapRequest'),
    url(r'^manage$', 'swap.views.manage'),
    url(r'^mustOverwrite$', 'swap.views.mustOverwrite'),
    url(r'^remove/(\d+)$', 'swap.views.remove'),

    # Examples:
    # url(r'^$', 'sectionswap.views.home', name='home'),
    # url(r'^sectionswap/', include('sectionswap.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'sectionswap.views.index'),
	url(r'^courses$', 'sectionswap.views.courses'),
	url(r'^swaprequest$', 'views.swapRequest'),
    url(r'^manage$', 'sectionswap.views.manage'),
    url(r'^mustOverwrite$', 'sectionswap.views.mustOverwrite'),
    url(r'^remove/(\d+)$', 'sectionswap.views.remove'),

    # Examples:
    # url(r'^$', 'sectionviews.home', name='home'),
    # url(r'^sectionswap/', include('sectionswap.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^login/?$', 'django_cas.views.login'),
    (r'^logout/?$', 'django_cas.views.logout'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

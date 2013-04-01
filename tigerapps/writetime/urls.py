from django.conf.urls.defaults import *
import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'writetime.views.index'),
    url(r'^offer$', 'writetime.views.offer'),
    url(r'^accept/(\d*)$', 'writetime.views.accept'),
    url(r'^submitOffer/$', 'writetime.views.submitOffer'),
    url(r'^submitAccept/(\d*)$', 'writetime.views.submitAccept'),
    url(r'^submitRemove/(\d*)$', 'writetime.views.submitRemove'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

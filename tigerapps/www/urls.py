from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^suggestions/?', direct_to_template, {'template': 'index/suggestions.html'}),
    url(r'^adam/?', direct_to_template, {'template': 'www/adam_box.html'}),
    url(r'^/?', direct_to_template, {'template': 'www/index.html'}),

    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

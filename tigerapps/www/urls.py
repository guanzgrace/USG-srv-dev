from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template
from django.contrib import admin

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/?', 'www.views.index'),
    url(r'^suggestions/?', direct_to_template, {'template': 'www/suggestions.html'}),

    url(r'^adam/?', direct_to_template, {'template': 'www/adam_box.html'}),
    url(r'^josh/?', direct_to_template, {'template': 'www/josh.html'}),

    # Admin
    url(r'^admin/?$', 'django_cas.views.login', kwargs={'next_page': '/djadmin/'}),
    (r'^djadmin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

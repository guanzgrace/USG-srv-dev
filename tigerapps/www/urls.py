from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template
from django.contrib import admin

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^suggestions/login/?',      'django_cas.views.login'),
    url(r'^suggestions/logout/?',    'django_cas.views.logout'),
    url(r'^suggestions/new/?',       'suggestions.views.submit_suggestion'),
    url(r'^suggestions/cast_vote/?', 'suggestions.views.cast_vote'),
    url(r'^suggestions/?$',          'suggestions.views.main_page'),

    url(r'^/?',                   'www.views.index'),

    # Admin
    url(r'^admin/?$', 'django_cas.views.login', kwargs={'next_page': '/djadmin/'}),
    (r'^djadmin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

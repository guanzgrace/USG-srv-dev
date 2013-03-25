from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Map-related
    url(r'^/?$', direct_to_template, {'template': 'pom/index.html'}),
    (r'^login/?$', 'django_cas.views.login'),
    (r'^logout/?$', 'django_cas.views.logout'),
    
    url(r'^refresh/?$', 'pom.views.refresh_cache'),

    url(r'^json/bldgs/names/?$', 'pom.views.get_bldg_names_json'),
    
    url(r'^bldgs/filter/?$', 'pom.views.bldgs_for_filter'),
    url(r'^data/bldg/(?P<bldg_code>\S+)/?$', 'pom.views.data_for_bldg'),
    url(r'^data/all/?$', 'pom.views.data_for_all'),

    url(r'^pmap/?$', direct_to_template,
        {'template': 'pom/pmap.html'}),

    #Admin
    url(r'^admin/?$', 'django_cas.views.login', kwargs={'next_page': '/djadmin/'}),
    (r'^djadmin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()


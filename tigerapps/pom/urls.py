from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Map-related
    url(r'^/?$', direct_to_template, {'template': 'pom/index.html'}),
    url(r'^about/?$', direct_to_template, {'template': 'pom/about.html'}),
    url(r'^refresh/?$', 'pom.views.refresh_cache'),


    url(r'^filtered/bldgs/?$', 'pom.views.get_filtered_bldgs'),
    url(r'^filtered/data/bldg/(?P<bldg_code>\S+)/?$', 'pom.views.get_filtered_data_bldg'),
    url(r'^filtered/data/all/?$', 'pom.views.get_filtered_data_all'),

    url(r'^widget/search/resp/?$', 'pom.views.widget_search/resp'),
    url(r'^widget/locations/setup/?$', 'pom.views.widget_locations_setup'),


    (r'^login/?$', 'django_cas.views.login'),
    (r'^logout/?$', 'django_cas.views.logout'),

    #Admin
    url(r'^admin/?$', 'django_cas.views.login', kwargs={'next_page': '/djadmin/'}),
    (r'^djadmin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()


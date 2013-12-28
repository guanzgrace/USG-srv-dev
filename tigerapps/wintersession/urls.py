from django.conf.urls import patterns, url
from wintersession import views

urlpatterns = patterns('',
    url(r'^enroll/$', views.enroll, name='enroll'),
    url(r'^student/$', views.student, name='student'),
    url(r'^courses/$', views.courses, name='courses'),
    url(r'^instructor/$', views.instructor, name='instructor'),
    url(r'^instructor/attendance$', views.instructor, name='attendance'),
    url(r'^student/drop/$', views.drop, name='drop'),
    url(r'^student/add/$', views.add, name='add'),
    url(r'^teach/$', views.teach, name='teach'),
    url(r'^about/$', views.about, name='about'),
    url(r'^$', views.home, name='home'),
    
    # login/logout
    #(r'^login/?$', 'django_cas.views.login'),
    #(r'^logout/?$', 'django_cas.views.logout'),
)

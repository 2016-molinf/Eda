from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.main_page, name='main_page'),
    url(r'^cas/$', views.aktualni_cas),
    url(r'^scitani/(\d{1,3})/(\d{1,3})/$', views.scitani),
    url(r'^chemdoodle/$', views.chemdoodle),
    url(r'^jsme/$', views.jsme),
    url(r'^search/$', views.search),
    url(r'^moldb_insert/$', views.moldb_insert),
    url(r'^all_search/$', views.all_search),
    url(r'^upload_sdf/$', views.upload_sdf),
    url(r'^successful_upload/$', views.successful_upload),
]
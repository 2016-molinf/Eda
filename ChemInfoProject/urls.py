"""ChemInfoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

# extra importy - web page logika/views
from ChemInfoProject.views import aktualni_cas, scitani, main_page, chemdoodle, jsme
#from ChemInfoProject.templates import main_page


# ||regexp na rozeznávání url (případně vytěžení nějakých proměnných)||, ||funkce ve views, která se pustí||
urlpatterns = [
    #url(r'^$', main_page),
    url(r'^', include('moldb.urls')),
    url(r'^admin/', admin.site.urls),
    #url(r'^cas/$', aktualni_cas),
    #url(r'^scitani/(\d{1,3})/(\d{1,3})/$', scitani),
    #url(r'^chemdoodle/$', chemdoodle),
    #url(r'^jsme/$', jsme),
]

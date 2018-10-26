"""Opendata URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Opendata.views import *
from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', home),
    url(r'^data/static/$', staticData),
    url(r'^data/realtime/$', dynamicData),
    url(r'^contact/$', contact),
    url(r'^about/$', about),
    url(r'^documentation/$', documentation),
    url(r'^terms/$', terms),
    url(r'^policy/$', policy),
    url(r'^privacy/$', privacy),
    path('admin/', admin.site.urls),

]

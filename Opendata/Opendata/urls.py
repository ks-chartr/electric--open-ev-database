
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
from EVUpdates.views import *
from django.urls import include, re_path


# admin.site.site_url = '/openev'

urlpatterns = [
    #re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', home),
    re_path(r'^data/static/$', staticData),
    re_path(r'^data/realtime/$', realtimeData),
    re_path(r'^data/provider/$', dataProvider),
    re_path(r'^contact/$', contact),
    re_path(r'^about/$', about),
    re_path(r'^documentation/$', documentation),
    re_path(r'^terms/$', terms),
    re_path(r'^policy/$', policy),
    re_path(r'^privacy/$', privacy),
    re_path(r'^announcements/$', announcement),
    re_path(r'^tinymce/', include('tinymce.urls')),
    re_path(r'^api/authenticate/', authenticate_api_key),
    re_path(r'^api/update-ev/', addUpdateEV),
    re_path(r'^api/update-stations/', addUpdateEV),
    re_path(r'^api/get-user-ev/', getMyEV),
    re_path(r'^api/get-user-stations/', getMyEV),
    re_path(r'^api/delete-station/', deleteEV),
    re_path(r'^api/get-ev/', getEV),

    re_path(r'^openev/$', home),
    re_path(r'^openev/data/static/$', staticData),
    re_path(r'^openev/data/realtime/$', realtimeData),
    re_path(r'^openev/data/provider/$', dataProvider),
    re_path(r'^openev/contact/$', contact),
    re_path(r'^openev/about/$', about),
    re_path(r'^openev/documentation/$', documentation),
    re_path(r'^openev/terms/$', terms),
    re_path(r'^openev/policy/$', policy),
    re_path(r'^openev/privacy/$', privacy),
    re_path(r'^openev/announcements/$', announcement),
    re_path(r'^openev/admin/', admin.site.urls),
    re_path(r'^openev/tinymce/', include('tinymce.urls')),
    re_path(r'^openev/api/authenticate/', authenticate_api_key),
    re_path(r'^openev/api/update-ev/', addUpdateEV),
    re_path(r'^openev/api/update-stations/', addUpdateEV),
    re_path(r'^openev/api/get-user-ev/', getMyEV),
    re_path(r'^openev/api/get-user-stations/', getMyEV),
    re_path(r'^openev/api/delete-station/', deleteEV),
    re_path(r'^openev/api/get-ev/', getEV),
    re_path(r'^openev/verify', verify_mobile_number)
]

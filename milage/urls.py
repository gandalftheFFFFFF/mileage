"""milage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from .views import index, create_user, log_out

urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^create-user/$', create_user, name='create-user'),
    url(r'^logout/$', log_out, name='logout'),
    url(r'^help/$', TemplateView.as_view(template_name='help.html'), name='help'),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^milage/', include('placeholder.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

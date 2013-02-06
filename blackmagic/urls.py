from django.conf.urls import patterns, include, url
from sonic_bar_code import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$', views.home, ),
    url(r'^upload$', views.upload_file, ),
    url(r'^generate', views.generate_view, ),
    url(r'^sounds/(?P<id>[0-9]+)/', views.view_past, )
)

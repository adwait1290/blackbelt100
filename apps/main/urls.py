from django.conf.urls import url
from django.contrib import admin
from . import views # This line is new!
urlpatterns = [
  url(r'^$', views.index), # This line has changed!
  url(r'^register/', views.register),
  url(r'^login', views.login, name="login"),
  url(r'^logout/', views.logout),
  url(r'^friends$', views.friends, name="friends"),
  url(r'^users/(?P<id>\d+)$', views.profile),
  url(r'^users/add/(?P<id>\d+)$', views.add_friend),
  url(r'^users/remove/(?P<id>\d+)$', views.remove_friend),
]



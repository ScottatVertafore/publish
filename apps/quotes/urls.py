from django.conf.urls import url, include
from . import views 
urlpatterns = [url(r'^$', views.index),
    url(r'^quotes$', views.quotes),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quote$', views.quote_add),
    url(r'^quote/(?P<quote_id>\d+)$', views.add_favorite),
    url(r'^remove/(?P<quote_id>\d+)$', views.delete_favorite) ,
    url(r'^users/(?P<user_id>\d+)$', views.users),
    url(r'^dashboard$', views.dashboard)
]
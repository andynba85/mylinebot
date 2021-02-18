from django.urls import path
#from newsbot import views
from .views import callback
from django.conf.urls import url

urlpatterns = [
    #path('callback', views.callback)
    url(r'^$',callback,name=callback)
]
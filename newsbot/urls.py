from django.urls import path
from newsbot import views

urlpatterns = [
    path('callback', views.callback)
]
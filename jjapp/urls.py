from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('calculate/', views.calculate, name = "calculate"),
    path('get_data/', views.get_data, name="get_data"),
    path('delete_data/', views.delete_data, name="delete_data"),
]
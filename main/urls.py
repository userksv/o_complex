from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:city>/', views.history, name='history'),
    path('api/statistics/', views.city_statistics, name='statistics'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('<slug:seccion>/', views.inicio, name='seccion'),
]

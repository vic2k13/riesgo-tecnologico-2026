from django.urls import path
from . import views

app_name = 'equipos'

urlpatterns = [
    path('', views.integrantes, name='integrantes'),
    path('responsable/', views.responsable, name='responsable'),
]

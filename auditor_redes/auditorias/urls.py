from django.urls import path
from . import views

app_name = 'auditorias'

urlpatterns = [
    path('', views.historial, name='historial'),
]

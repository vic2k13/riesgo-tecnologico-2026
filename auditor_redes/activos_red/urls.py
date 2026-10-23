from django.urls import path
from . import views

app_name = 'activos_red'

urlpatterns = [
    path('', views.inventario, name='inventario'),
    path('segmentos/', views.segmentos, name='segmentos'),
]

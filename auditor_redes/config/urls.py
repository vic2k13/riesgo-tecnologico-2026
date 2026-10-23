from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # La raíz redirige al resumen del panel y define el nombre 'inicio'
    path('', RedirectView.as_view(pattern_name='panel:resumen', permanent=False), name='inicio'),

    path('panel/', include('panel.urls')),
    path('herramientas/', include('activos_red.urls')),
    path('equipos/', include('equipos.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('auditorias/', include('auditorias.urls')),
    path('documentacion/', TemplateView.as_view(template_name='documentacion.html'), name='documentacion'),
]

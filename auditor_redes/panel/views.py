from django.http import Http404
from django.shortcuts import render


EQUIPO_NOMBRE = 'Equipo 1'
INTEGRANTES_EQUIPO = (
    {
        'nombre': 'Gretel Alexandra Lugo Díaz Ordaz',
        'correo': 'grets1@ciencias.unam.mx',
        'iniciales': 'GL',
        'tono': 'violeta',
    },
    {
        'nombre': 'Arlet Pinacho Báez',
        'correo': 'arlet.pinacho@ciencias.unam.mx',
        'iniciales': 'AP',
        'tono': 'verde',
    },
    {
        'nombre': 'Luis Israel Carrillo Gónzalez',
        'correo': 'luiscarrillo@ciencias.unam.mx',
        'iniciales': 'LC',
        'tono': 'naranja',
    },
    {
        'nombre': 'Diego Hazael Vega Alonso',
        'nombres': 'Diego Hazael',
        'apellidos': 'Vega Alonso',
        'saludo': 'Diego',
        'correo': 'diegohazael2005@ciencias.unam.mx',
        'iniciales': 'DV',
        'tono': 'azul',
    },
)
# Perfil mostrado en la maqueta; no representa una sesión autenticada.
USUARIO_PANEL = INTEGRANTES_EQUIPO[-1]


MENU_JR = (
    {'clave': 'panel', 'nombre': 'Panel', 'submenus': (('resumen', 'Resumen'), ('actividad', 'Actividad reciente'))},
    {'clave': 'herramientas', 'nombre': 'Herramientas', 'submenus': (('puertos', 'Verificación de puertos'), ('dispositivos', 'Dispositivos conectados'))},
    {'clave': 'mi-equipo', 'nombre': 'Mi equipo', 'submenus': (('integrantes', 'Integrantes'), ('responsable', 'Auditor responsable'))},
    {'clave': 'mi-usuario', 'nombre': 'Mi usuario', 'submenus': (('perfil', 'Mi perfil'), ('cuenta', 'Datos de la cuenta'))},
    {'clave': 'historial', 'nombre': 'Historial', 'submenus': (('auditorias', 'Mis auditorías'),)},
    {'clave': 'documentacion', 'nombre': 'Documentación', 'submenus': (('guias', 'Guías de uso'), ('referencia', 'Referencia rápida'))},
    {'clave': 'cerrar-sesion', 'nombre': 'Cerrar sesión', 'submenus': (('sesion', 'Mi sesión'),)},
)

AUDITORIAS_EJEMPLO = (
    {'folio': 'AUD-012', 'nombre': 'Revisión de red local', 'herramienta': 'Verificación de puertos', 'fecha': '20 oct 2026', 'estado': 'En progreso', 'color': 'azul'},
    {'folio': 'AUD-011', 'nombre': 'Inventario de dispositivos', 'herramienta': 'Dispositivos conectados', 'fecha': '19 oct 2026', 'estado': 'En revisión', 'color': 'amarillo'},
    {'folio': 'AUD-010', 'nombre': 'Revisión de servicios', 'herramienta': 'Verificación de puertos', 'fecha': '18 oct 2026', 'estado': 'Completada', 'color': 'verde'},
    {'folio': 'AUD-009', 'nombre': 'Reconocimiento de red', 'herramienta': 'Dispositivos conectados', 'fecha': '16 oct 2026', 'estado': 'Completada', 'color': 'verde'},
)


def inicio(request, seccion='panel'):
    opcion = next((item for item in MENU_JR if item['clave'] == seccion), None)
    if opcion is None:
        raise Http404('La sección no existe.')

    anclas = [ancla for ancla, nombre in opcion['submenus']]
    subseccion_activa = request.GET.get('subseccion', anclas[0])
    if subseccion_activa not in anclas:
        subseccion_activa = anclas[0]

    contexto = {
        'menu_jr': MENU_JR,
        'seccion_activa': seccion,
        'subseccion_activa': subseccion_activa,
        'seccion': opcion,
        'plantilla_seccion': f'panel/secciones/{seccion}.html',
        'auditorias': AUDITORIAS_EJEMPLO,
        'equipo_nombre': EQUIPO_NOMBRE,
        'integrantes': INTEGRANTES_EQUIPO,
        'usuario_panel': USUARIO_PANEL,
    }
    return render(request, 'panel/inicio.html', contexto)

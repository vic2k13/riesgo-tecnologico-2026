from django.urls import reverse, NoReverseMatch


def _resolver(nombre_url):
    """Devuelve la URL o '#' si aún no existe (útil mientras construyes las apps)."""
    try:
        return reverse(nombre_url)
    except NoReverseMatch:
        return "#"


# prefix = comienzo de la ruta que identifica a la sección (para marcarla como activa).
# Debe coincidir con la ruta donde montas cada app en config/urls.py.
MENU = [
    {
        "label": "Panel",
        "prefix": "/panel/",
        "url": "panel:resumen",
        "items": [
            {"label": "Resumen", "url": "panel:resumen"},
        ],
    },
    {
        "label": "Herramientas",
        "prefix": "/herramientas/",
        "url": "activos_red:inventario",
        "items": [
            {"label": "Inventario de activos", "url": "activos_red:inventario"},
            {"label": "Segmentos autorizados", "url": "activos_red:segmentos"},
        ],
    },
    {
        "label": "Mi equipo",
        "prefix": "/equipos/",
        "url": "equipos:integrantes",
        "items": [
            {"label": "Integrantes", "url": "equipos:integrantes"},
            {"label": "Auditor responsable", "url": "equipos:responsable"},
        ],
    },
    {
        "label": "Mi usuario",
        "prefix": "/usuarios/",
        "url": "usuarios:perfil",
        "items": [
            {"label": "Mi perfil", "url": "usuarios:perfil"},
        ],
    },
    {
        "label": "Historial",
        "prefix": "/auditorias/",
        "url": "auditorias:historial",
        "items": [
            {"label": "Mis auditorías", "url": "auditorias:historial"},
        ],
    },
    {
        "label": "Documentación",
        "prefix": "/documentacion/",
        "url": "documentacion",
        "items": [],
    },
]


def menu_principal(request):
    path = request.path
    secciones = []
    activa = None

    for seccion in MENU:
        es_activa = path.startswith(seccion["prefix"])
        items = []
        for i in seccion["items"]:
            href = _resolver(i["url"])
            items.append({"label": i["label"], "href": href, "activo": href == path})
        data = {
            "label": seccion["label"],
            "href": _resolver(seccion["url"]),
            "activa": es_activa,
            "items": items,
        }
        if es_activa:
            activa = data
        secciones.append(data)

    return {"menu_secciones": secciones, "menu_activa": activa}

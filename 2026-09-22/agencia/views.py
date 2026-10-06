from django.shortcuts import render

# Diccionario que define A (llaves) y B (listas/valores).
#B se puede ver como si fueran subtemas
#tema1': ['subtema1.1', 'subtema1.2', 'subtema1.3'],
#tema2': ['subtema2.1', 'subtema2.2', 'subtema2.3'],
MENU = {
    'Ventas': ['Nuevos', 'Seminuevos', 'Garantias'],
    'Mecanico': ['Mantenimiento', 'Motor', 'Frenos'],
    'Refacciones': ['Aceites', 'Filtros', 'Llantas'],
    'Hojalateria': ['Pintura', 'Abolladuras']
}


#{% url 'agencia:inicio' %}
def inicio(request):
    return render(request, 'agencia/inicio.html', {'menu_a': MENU.keys()})

#Vamos a recibir como parámetro de la url la var servicio
def seccion(request, servicio):
    #Obtenemos el listado de subtemas
    opciones_b = MENU.get(servicio, [])
    contexto = {
        'menu_a': MENU.keys(),
        #Metemos al contexto el servicio secundario (subtema)
        'servicio_activo': servicio,
        #También mandamos la lista de servicios secundarios (subtemas)
        'opciones_b': opciones_b
    }
    #Respondemos a la petición con el .html y el contexto
    return render(request, 'agencia/inicio.html', contexto)

#Función que regresa un html dependiendo del subtema seleccionado
def obtener_html_subtema(subtema):
    match subtema:
        case 'Nuevos':
            return 'agencia/ventas/nuevos.html'
        case 'Seminuevos':
            return 'agencia/ventas/seminuevos.html'
        case 'Garantias':
            return 'agencia/ventas/garantias.html'
        case 'Mantenimiento':
            return 'agencia/mantenimiento.html'
        case 'Motor':
            return 'agencia/motor.html'
        case 'Frenos':
            return 'agencia/frenos.html'
        case 'Aceites':
            return 'agencia/algun.html'
        case 'Filtros':
            return 'agencia/algun.html'
        case 'Llantas':
            return 'agencia/algun.html'
        case 'Pintura':
            return 'agencia/algun.html'
        case 'Abolladuras':
            return 'agencia/algun.html'
        case _:
            return 'agencia/error.html'


#Vamos a recibir como parámetro de la url las vars servicio y subtema
def detalle(request, servicio, subtema):
    #Obtenemos el listado de subtemas
    opciones_b = MENU.get(servicio, [])
    contexto = {
        'menu_a': MENU.keys(),
        'servicio_activo': servicio,
        'opciones_b': opciones_b,
        'subtema_activo': subtema
    }

    #return render(request, 'agencia/detalle.html', contexto)
    #Actividad
    
    respuesta_html = obtener_html_subtema(subtema)
    return render(request, respuesta_html, contexto)
    
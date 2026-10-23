from django.shortcuts import render


def inventario(request):
    return render(request, 'activos_red/inventario.html')

def segmentos(request):
    return render(request, 'activos_red/segmentos.html')

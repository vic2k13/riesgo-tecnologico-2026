from django.shortcuts import render


def integrantes(request):
    return render(request, 'equipos/integrantes.html')

def responsable(request):
    return render(request, 'equipos/responsable.html')

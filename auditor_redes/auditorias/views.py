from django.shortcuts import render


def historial(request):
    return render(request, 'auditorias/historial.html')

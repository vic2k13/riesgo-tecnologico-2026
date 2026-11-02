from django.shortcuts import render


def resumen(request):
    return render(request, 'panel/resumen.html')

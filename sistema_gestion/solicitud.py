from django.shortcuts import render, redirect
from .models import solicitud

def inicio_solicitud(request):
    solicitudes = solicitud.objects.all()
    context = {'solicitudes': solicitudes}
    return render(request, 'paginas/', context)
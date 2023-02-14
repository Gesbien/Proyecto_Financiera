from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import  ListView, CreateView

from .models import solicitud
from .personas import registroPersona

def inicio_solicitud(request):
    solicitudes = solicitud.objects.all()
    context = {'solicitudes': solicitudes}
    return render(request, 'paginas/gestionSolicitud.html', context)

def crear_solicitud(request):
    return render(request, "paginas/registrarSolicitud.html")

def registroSolicitud(request):
    salida = 'Solicitud'
    cedula_info = registroPersona(request,salida)
    monto = request.POST['txt_monto']
    estado = 'Proceso'

    Solicitud = solicitud.objects.create(cedula=cedula_info,monto=monto,estado=estado)

    return redirect('/solicitud')

def editarSolicitud(request, id_solicitud):
    Solicitud = solicitud.objects.get(id_solicitud=id_solicitud)
    data = {
        'solicitud': Solicitud
    }
    return render(request, "paginas/edicionSolicitud.html", data)

def edicionSolicitud(request):
    id_solicitud = request.POST['txtId_Solicitud']
    estado = request.POST['txtEstado']
    monto = request.POST['numMonto']
    tasa = request.POST['numTasa']
    cuota = request.POST['numCuota']


    Solicitud = solicitud.objects.get(id_solicitud=id_solicitud)
    Solicitud.estado = estado
    Solicitud.monto = monto
    Solicitud.tasa = tasa
    Solicitud.cuota = cuota
    Solicitud.save()

    return redirect('/solicitud')

def eliminacionSolicitud(request, id_solicitud):
    Solicitud = solicitud.objects.get(id_solicitud=id_solicitud)
    Solicitud.estado = 'Anulado'
    Solicitud.save()

    return redirect('/solicitud')
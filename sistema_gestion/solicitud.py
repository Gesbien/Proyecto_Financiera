from django.shortcuts import render, redirect, get_object_or_404
from .models import solicitud
from .models import persona

def inicio_solicitud(request):
    solicitudes = solicitud.objects.all()
    context = {'solicitudes': solicitudes}
    return render(request, 'paginas/gestionSolicitud.html', context)

def crear_solicitud(request):
    return render(request, "paginas/registrarSolicitud.html")

def registroSolicitud(request):
    id_solicitud = request.POST['txtId_Solicitud']
    estado = request.POST['txtEstado']
    monto = request.POST['numMonto']
    tasa = request.POST['numTasa']
    cuota = request.POST['numCuota']

    Solicitud = solicitud.objects.create(id_solicitud=id_solicitud, estado=estado, monto=monto,
                                         tasa=tasa, cuota=cuota)
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
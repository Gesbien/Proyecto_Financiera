from django.shortcuts import render, redirect
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
    return redirect('registrarSolicitud/')
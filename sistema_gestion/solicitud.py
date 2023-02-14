from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import  ListView, CreateView

from .models import solicitud, persona, informacion_trabajo

def inicio_solicitud(request):
    solicitudes = solicitud.objects.all()
    context = {'solicitudes': solicitudes}
    return render(request, 'paginas/gestionSolicitud.html', context)

def crear_solicitud(request):
    return render(request, "paginas/registrarSolicitud.html")

def registroSolicitud(request):
    cedula = request.POST.get('txtCedula')
    nombres = request.POST["txt_nombres"]
    apellidos = request.POST["txt_apellidos"]
    direccion = request.POST["txt_direccion"]
    telefono = request.POST["txt_telefono"]
    celular = request.POST["txt_celular"]
    tipo = 'Solicitante'
    estado = 'Activo'

    Persona = persona.objects.create(cedula=cedula, nombres=nombres,
                                     apellidos=apellidos,
                                     direccion=direccion, telefono=telefono, celular=celular, tipo=tipo, estado=estado)
    cedula_info = Persona
    monto = request.POST('txt_monto')
    estado = 'Proceso'

    Solicitud = solicitud.objects.create(cedula=cedula_info,monto=monto,estado=estado)

    nombre_trabajo = request.POST['txt_trabj_nombre']
    telefono_trabajo = request.POST['txt_trabj_direccion']
    direccion_trabajo = request.POST['txt_trabj_telefono']
    sueldo = request.POST['txt_trabj_sueldo']

    info = informacion_trabajo.objects.create(cedula=cedula_info, nombre=nombre_trabajo,
                                              telefono=telefono_trabajo, direccion=direccion_trabajo,
                                              sueldo=sueldo)

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
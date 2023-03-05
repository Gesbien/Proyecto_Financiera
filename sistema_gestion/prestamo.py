from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import prestamo, solicitud
from .garantia import registroGarantia
from .personas import registroPersona

def inicio_prestamo(request):
    prestamos = prestamo.objects.all().exclude(estado='Anulado')
    solicitudes = solicitud.objects.all().filter(estado='Aceptada')
    context = {
        'solicitudes' : solicitudes,
        'prestamos': prestamos}
    return render(request, 'paginas/gestionPrestamo.html', context)

def crear_prestamo(request,id_solicitud):
    Solicitud = solicitud.objects.get(id_solicitud=id_solicitud)
    Num_prestamo = 1
    context = {
        'opcion'    : 'nv',
        'solicitud' : Solicitud,
        'numero'    : Num_prestamo
    }
    return render(request, "paginas/registrarPrestamo.html", context)

def registroPrestamo(request,opcion,id_solicitud):
    salida = 'Prestamo'
    monto = request.POST['txt_monto']
    tasa = request.POST['txt_tasa']
    cuota = request.POST['txt_cuota']
    clasificacion = request.POST['txt_clasificacion']
    porciento_mora = request.POST['txt_%_de_mora']
    dias_gracia = request.POST['txt_dias_de_gracia']
    valor_cuota = request.POST['txt_valor_cuota']
    fecha = request.POST['datepicker-month_inicio']
    fecha_exped = datetime.strptime(fecha, '%m/%d/%Y')
    fecha_convert = fecha_exped.strftime('%Y-%m-%d')
    fecha_fin = request.POST['fecha_fin']
    estado = 'Proceso'
    Solicitud = solicitud.objects.get(id_solicitud=id_solicitud)
    Prestamo = prestamo.objects.create(id_solicitud=Solicitud,fecha_expedicion=fecha_convert,fecha_expiracion=fecha_fin,dias_gracia=dias_gracia,
                                      clasificacion=clasificacion,estado=estado,valor_cuota=valor_cuota,cuota=cuota,
                                       tasa=tasa,monto=monto,porciento_mora=porciento_mora)
    if opcion == 'nv':
        tipo = request.POST.get('roleSel')
        if tipo == 'Garante':
            registroPersona(request,tipo)
        else:
            registroGarantia(request,salida)

    return redirect('/prestamo')

def editarPrestamo(request, id_prestamo):
    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    data = {
        'Prestamo': prestamo
    }
    return render(request, "paginas/edicionPrestamo.html",data)

def edicionPrestamo(request):
    id_solicitud = request.POST['txtId_Solicitud']
    id_prestamo = request.POST['txtId_Prestamo']
    estado = request.POST['txtEstado']
    monto = request.POST['numMonto']
    tasa = request.POST['numTasa']
    cuota = request.POST['numCuota']


    Prestamo = prestamo.objects.get(id_solicitud=id_solicitud)
    Prestamo.estado = estado
    Prestamo.monto = monto
    Prestamo.tasa = tasa
    Prestamo.cuota = cuota
    Prestamo.save()

    return redirect('/prestamo')

def anulacionPrestamo(request, id_prestamo):
    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    Prestamo.estado = 'Anulado'
    Prestamo.save()

    return redirect('/prestamo')
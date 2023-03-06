from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import prestamo, solicitud, prestamo_garantia, garante, informacion_trabajo
from .garantia import registroGarantia, edicionGarantia
from .personas import registroPersona, edicionPersona

def inicio_prestamo(request):
    prestamos = prestamo.objects.all().exclude(estado='Anulado')
    solicitudes = solicitud.objects.all().filter(estado='Aceptada')
    context = {
        'solicitudes' : solicitudes,
        'prestamos': prestamos}
    return render(request, 'paginas/gestionPrestamo.html', context)

def crear_prestamo(request,id_solicitud):
    Solicitud = solicitud.objects.get(id_solicitud=id_solicitud)
    if prestamo.objects.last() is not None:
        Num_prestamo = 1 + prestamo.objects.last().id_prestamo
    else:
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
    clasificacion = request.POST.get('typeSel')
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
    Solicitud.estado = 'Procesada'
    Solicitud.save()
    if opcion == 'nv':
        tipo = request.POST.get('roleSel')
        if tipo == 'Garante':
           Persona = registroPersona(request,tipo)
           garante.objects.create(id_prestamo=Prestamo,id_persona=Persona)
        else:
            Garantia = registroGarantia(request,salida)
            prestamo_garantia.objects.create(id_prestamo=Prestamo, id_garantia=Garantia.id_garantia)

    return redirect('/prestamo')

def editarPrestamo(request, id_prestamo):
    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    Solicitud = Prestamo.id_solicitud

    if Prestamo.clasificacion == 'Personal':
        Union_Garante = garante.objects.get(id_prestamo=Prestamo)
        Trabajo = informacion_trabajo.objects.get(cedula=Union_Garante.id_persona)
        context = {
            'garante': Union_Garante,
            'solicitud': Solicitud,
            'prestamo': Prestamo,
            'trabajo'  : Trabajo
        }
    else:
        Union_Garantia = prestamo_garantia.objects.get(id_prestamo=id_prestamo)
        context = {
            'garantia': Union_Garantia,
            'solicitud': Solicitud,
            'prestamo': Prestamo
        }

    return render(request, "paginas/edicionPrestamo.html",context)

def edicionPrestamo(request,id_prestamo):
    salida = 'Prestamo'
    monto = request.POST['txt_monto']
    tasa = request.POST['txt_tasa']
    cuota = request.POST['txt_cuota']
    porciento_mora = request.POST['txt_%_de_mora']
    dias_gracia = request.POST['txt_dias_de_gracia']
    valor_cuota = request.POST['txt_valor_cuota']
    fecha = request.POST['datepicker-month_inicio']
    fecha_exped = datetime.strptime(fecha, '%m/%d/%Y')
    fecha_convert = fecha_exped.strftime('%Y-%m-%d')
    fecha_fin = request.POST['fecha_fin']

    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    Prestamo.monto = monto
    Prestamo.tasa = tasa
    Prestamo.cuota = cuota
    Prestamo.porciento_mora = porciento_mora
    Prestamo.dias_gracia = dias_gracia
    Prestamo.valor_cuota = valor_cuota
    Prestamo.fecha_expedicion = fecha_convert
    Prestamo.fecha_expiracion = fecha_fin
    Prestamo.save()

    tipo = request.POST['txt_clasificacion']
    if tipo == 'Personal':
        edicionPersona(request, salida)
    elif tipo == 'Inmobiliario' or tipo == 'Vehiculo':
        Garantia = prestamo_garantia.objects.get(id_prestamo=id_prestamo)
        edicionGarantia(request, salida,Garantia.id_garantia.id_garantia )

    return redirect('/prestamo')

def anulacionPrestamo(request, id_prestamo):
    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    Prestamo.estado = 'Anulado'
    Prestamo.save()

    return redirect('/prestamo')
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import  ListView, CreateView

from .models import desembolso,prestamo, persona, solicitud
from .personas import registroPersona

def inicio_desmbolso(request):
    desmbolso = desembolso.objects.all()
    context = {'desmbolso': desmbolso}
    return render(request, 'paginas/gestionDesembolso.html', context)

def crear_desembolso(request,id_prestamo):
    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    Solicitud = solicitud.objects.get(id_solicitud=Prestamo.id_solicitud.id_solicitud)
    Persona = persona.objects.get(cedula=Solicitud.cedula.cedula)
    if desembolso.objects.last() is not None:
        Num_desembolso = 1 + desembolso.objects.last().id_prestamo
    else:
        Num_desembolso = 1
    context = {
            'prestamo' : Prestamo,
            'cliente'  : Persona,
            'numero'   : Num_desembolso
    }
    return render(request, "paginas/registrarDesembolso.html", context)

def registroDesembolso(request,id_prestamo):
    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    monto = request.POST['txt_Monto']
    codigo_cuenta_cheque = request.POST['txt_num']
    cuota = request.POST['txt_cuota']
    fecha = request.POST['datepicker-month_inicio']
    fecha_exped = datetime.strptime(fecha, '%m/%d/%Y')
    fecha_convert = fecha_exped.strftime('%Y-%m-%d')
    estado = 'Activo'
    orden_de = request.POST['txt_Nombres']
    tipo = request.POST['txt_tipo']


    Desembolso = desembolso.objects.create( id_prestamo = Prestamo  ,monto_total=monto,estado=estado,codigo_cuenta_cheque=codigo_cuenta_cheque,cuota=cuota,
                                            fecha = fecha_convert, cliente = orden_de, tipo = tipo )

    return redirect('/prestamo')

def editarDesembolso(request, id_desembolso):
    Desmbolso = desembolso.objects.get(id_desembolso=id_desembolso)
    data = {
        'Desembolso': desembolso
    }
    return render(request, "paginas/edicionDesembolso.html", data)

def edicionDesembolso(request):
    id_solicitud = request.POST['txtId_Solicitud']
    id_prestamo = request.POST['txtId_Prestamo']
    estado = request.POST['txtEstado']
    monto_total = request.POST['numMonto_Total']
    codigo_cuenta_cheque = request.POST['txtCodigo_cuenta_cheque']



    Desembolso = desembolso.objects.get(id_solicitud=id_solicitud)
    Desembolso.id_prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    Desembolso.codigo_cuenta_cheque = codigo_cuenta_cheque
    Desembolso.estado = estado
    Desembolso.monto = monto_total
    Desembolso.save()

    return redirect('/prestamo')

def eliminacionPrestamo(request, id_desembolso):
    Desembolso = desembolso.objects.get(id_desembolso=id_desembolso)
    Desembolso.estado = 'Anulado'
    Desembolso.save()

    return redirect('/desembolso')
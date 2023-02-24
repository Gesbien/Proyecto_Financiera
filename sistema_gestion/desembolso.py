from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import  ListView, CreateView

from .models import desembolso,prestamo
from .personas import registroPersona

def inicio_desmbolso(request):
    desmboloso = desembolso.objects.all()
    context = {'desmbolso': desmboloso}
    return render(request, 'paginas/gestionDesembolso.html', context)

def crear_desembolso(request):
    return render(request, "paginas/registrarDesembolso.html")

def registroDesembolso(request,prestamo):
    monto_total = request.POST['txt_monto_total']
    codigo_cuenta_cheque = request.POST['txt_tasa']
    cuota = request.POST['txt_cuota']
    estado = 'Proceso'


    Desembolso = desembolso.objects.create( id_prestamo =prestamo  ,monto_total=monto_total,estado=estado,codigo_cuenta_cheque=codigo_cuenta_cheque,cuota=cuota)

    return redirect('/prestamo')

def editarDesembolso(request, id_desmbolso):
    Desmbolso = desembolso.objects.get(id_desembolso=id_desmbolso)
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
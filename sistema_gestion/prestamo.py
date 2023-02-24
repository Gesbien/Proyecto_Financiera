from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import  ListView, CreateView

from .models import prestamo
from .personas import registroPersona

def inicio_prestamo(request):
    prestamos = prestamo.objects.all()
    context = {'prestamo': prestamos}
    return render(request, 'paginas/gestionPrestamos.html', context)

def crear_prestamo(request):
    return render(request, "paginas/registrarPrestamo.html")

def registroPrestamo(request):
    salida = 'Prestamo'
    cedula_info = registroPersona(request,salida)
    monto = request.POST['txt_monto']
    tasa = request.POST['txt_tasa']
    cuota = request.POST['txt_cuota']
    estado = 'Proceso'


    Prestamo = prestamo.objects.create(cedula=cedula_info,monto=monto,estado=estado,tasa=tasa,cuota=cuota)

    return redirect('/prestamo')

def editarPrestamo(request, id_prestamo):
    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    data = {
        'Prestamo': prestamo
    }
    return render(request, "paginas/edicionPrestamo.html", data)

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

def eliminacionPrestamo(request, id_prestamo):
    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    Prestamo.estado = 'Anulado'
    Prestamo.save()

    return redirect('/prestamo')
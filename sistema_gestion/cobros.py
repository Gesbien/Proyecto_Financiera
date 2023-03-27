from datetime import datetime
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import prestamo, cobro

def inicio_cobros(request):
    Cobros = cobro.objects.all()
    Prestamos = prestamo.objects.all().filter(estado='Desembolsado')
    paginator = Paginator(Cobros, 10)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    context = {'items': items,
               'prestamos' : Prestamos}
    return render(request, 'paginas/gestionCobro.html', context)

def crear_cobro(request,id_prestamo):
    if cobro.objects.last() is not None:
        Num_cobro = 1 + cobro.objects.last().id_cobro
    else:
        Num_cobro = 1

    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    monto_interes = Prestamo.balance_interes/Prestamo.cuota
    monto_capital = Prestamo.balance_capital/Prestamo.cuota
    context = {
        'num_cobro': Num_cobro,
        'prestamo': Prestamo,
        'interes' : monto_interes,
        'capital' : monto_capital
    }

    return render(request, "paginas/registrarCobro.html", context)

def registro_cobros(request,id_cobro):
    id_prestamo = request.POST['txt_prestamos']
    monto_total = request.POST['txt_monto_total']
    monto_interes = request.POST['txt_monto_interes']
    monto_capital = request.POST['txt_monto_capital']
    concepto = request.POST['txt_concepto']
    fecha = request.POST['txt_fecha']
    fecha_exped = datetime.strptime(fecha, '%m/%d/%Y')
    fecha_convert = fecha_exped.strftime('%Y-%m-%d')
    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    estado = 'Realizado'

    cobro.objects.create(id_cobro=id_cobro,monto_total=monto_total,monto_interes=monto_interes,
                         monto_capital=monto_capital,concepto=concepto,fecha=fecha_convert,
                         id_prestamo=Prestamo, estado=estado)

    return redirect('/cobros')

def editar_cobro(request,id_cobro):
    Cobro = cobro.objects.get(id_cobro=id_cobro)
    context = {
        'cobro': Cobro,
    }
    return render(request, "paginas/edicionCobro.html", context)

def edicion_cobros(request,id_cobro):
    monto_total = request.POST['txt_monto_total']
    monto_interes = request.POST['txt_monto_interes']
    monto_capital = request.POST['txt_monto_capital']
    concepto = request.POST['txt_concepto']
    fecha = request.POST['txt_fecha']
    fecha_exped = datetime.strptime(fecha, '%m/%d/%Y')
    fecha_convert = fecha_exped.strftime('%Y-%m-%d')

    Cobro = cobro.objects.get(id_cobro=id_cobro)
    Cobro.monto_total = monto_total
    Cobro.monto_interes = monto_interes
    Cobro.monto_capital = monto_capital
    Cobro.concepto = concepto
    Cobro.fecha = fecha_convert
    Cobro.save()

    return redirect('/cobros')

def postear_cobros(request,id_cobro):
    Cobro = cobro.objects.get(id_cobro=id_cobro)
    Cobro.estado = 'Posteado'
    Cobro.save()
    Prestamo = prestamo.objects.get(id_prestamo=Cobro.id_prestamo.id_prestamo)

    Prestamo.balance_actual -= Cobro.monto_total
    Prestamo.balance_capital -= Cobro.monto_capital
    Prestamo.balance_interes -= Cobro.monto_interes
    Prestamo.save()

    return redirect('/cobros')

def anulacion_cobros(request, id_cobro):
    Cobro = cobro.objects.get(id_cobro=id_cobro)
    Cobro.estado = 'Anulado'
    Cobro.save()

    return redirect('/cobros')

def tabla_amortizacion(id_prestamo):
    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    monto = Prestamo.monto
    tasa = Prestamo.tasa
    cuota = Prestamo.cuota
    monto_interes = Prestamo.balance_interes
    pago_interes = monto_interes / cuota
    pago_capital = monto / cuota
    valor_cuota = Prestamo.valor_cuota
    balance_total = Prestamo.balance_actual
    i = 0






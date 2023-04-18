from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import prestamo, cobro, tabla_amortizacion
from reportlab.pdfgen import canvas

def inicio_cobros(request):
    Cobros = cobro.objects.all()
    Prestamos = prestamo.objects.all().filter(estado='Desembolsado')
    paginator = Paginator(Cobros, 10)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    context = {'items': items,
               'prestamos' : Prestamos}
    return render(request, 'paginas/gestionCobro.html', context)

def actualizar_prestamo(fecha_hoy,Prestamo):
    mora = 0
    cont = 0
    tabla = tabla_amortizacion.objects.all().filter(id_prestamo=Prestamo.id_prestamo)

    for item in tabla:
        fecha_limite = item.fecha + timedelta(days=Prestamo.dias_gracia)
        if Prestamo.balance_actual <= item.balance_actual:
            item.estado = 'Pagado'
            item.save()
        elif fecha_limite < datetime.strptime('2023-05-23','%Y-%m-%d').date():
            cont += 1
            item.estado = 'Atrasado'
            item.save()
            mora = item.cuota * (Prestamo.porciento_mora/100)
        else:
            cont += 1
            item.estado = 'Activo'
            item.save()

    Prestamo.cuota_faltantes = cont
    Prestamo.save()

    return round(mora,2)

def crear_cobro(request,id_prestamo):
    if cobro.objects.last() is not None:
        Num_cobro = 1 + cobro.objects.last().id_cobro
    else:
        Num_cobro = 1

    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    tabla_amortizada = tabla_amortizacion.objects.all().filter(id_prestamo=id_prestamo)
    fecha_hoy = datetime.today()
    fecha = fecha_hoy.strftime('%Y-%m-%d')
    mora = actualizar_prestamo(fecha,Prestamo)
    fecha_convert = fecha_hoy.strftime('%m/%d/%Y')
    monto_total = (Prestamo.balance_actual/Prestamo.cuota_faltantes) + mora
    monto_interes = Prestamo.balance_interes / Prestamo.cuota_faltantes
    monto_capital = monto_total - monto_interes
    context = {
        'num_cobro': Num_cobro,
        'prestamo': Prestamo,
        'interes' : monto_interes,
        'capital' : monto_capital,
        'tabla'   : tabla_amortizada,
        'fecha'   : fecha_convert,
        'mora'    : mora,
        'monto_tot' : monto_total
    }

    return render(request, "paginas/registrarCobro.html", context)

def registro_cobros(request,id_cobro):
    id_prestamo = request.POST['txt_prestamos']
    monto_total = request.POST['txt_monto_total']
    monto_interes = request.POST['txt_monto_interes']
    monto_capital = request.POST['txt_monto_capital']
    monto_mora  = request.POST['txt_mora']
    concepto = request.POST['txt_concepto']
    fecha = request.POST['txt_fecha']
    fecha_exped = datetime.strptime(fecha, '%m/%d/%Y')
    fecha_convert = fecha_exped.strftime('%Y-%m-%d')
    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    estado = 'Realizado'

    cobro.objects.create(id_cobro=id_cobro,monto_total=monto_total,monto_interes=monto_interes,
                         monto_capital=monto_capital,concepto=concepto,fecha=fecha_convert,
                         id_prestamo=Prestamo,monto_mora=monto_mora, estado=estado)

    return redirect('/cobros')

def editar_cobro(request,id_cobro):
    Cobro = cobro.objects.get(id_cobro=id_cobro)
    tabla_amortizada = tabla_amortizacion.objects.all().filter(id_prestamo=Cobro.id_prestamo.id_prestamo)
    context = {
        'cobro': Cobro,
        'tabla': tabla_amortizada
    }
    return render(request, "paginas/edicionCobro.html", context)

def edicion_cobros(request,id_cobro):
    monto_total = request.POST['txt_monto_total']
    monto_interes = request.POST['txt_monto_interes']
    monto_capital = request.POST['txt_monto_capital']
    monto_mora  = request.POST['txt_mora']
    concepto = request.POST['txt_concepto']
    fecha = request.POST['txt_fecha']
    fecha_exped = datetime.strptime(fecha, '%m/%d/%Y')
    fecha_convert = fecha_exped.strftime('%Y-%m-%d')

    Cobro = cobro.objects.get(id_cobro=id_cobro)
    Cobro.monto_total = monto_total
    Cobro.monto_interes = monto_interes
    Cobro.monto_capital = monto_capital
    Cobro.monto_mora = monto_mora
    Cobro.concepto = concepto
    Cobro.fecha = fecha_convert
    Cobro.save()

    return redirect('/cobros')

def postear_cobros(request,id_cobro):
    Cobro = cobro.objects.get(id_cobro=id_cobro)
    Cobro.estado = 'Posteado'
    Cobro.save()
    Prestamo = prestamo.objects.get(id_prestamo=Cobro.id_prestamo.id_prestamo)
    tabla = tabla_amortizacion.objects.all().filter(id_prestamo=Prestamo).exclude(estado='Pagado')
    Prestamo.balance_actual -= (Cobro.monto_total - Cobro.monto_mora)
    Prestamo.balance_capital -= Cobro.monto_capital
    Prestamo.balance_interes -= Cobro.monto_interes
    Prestamo.balance_mora += Cobro.monto_mora
    Prestamo.save()

    for item in tabla:
        if Prestamo.balance_actual <= item.balance_actual:
            item.estado = 'Pagado'
            item.save()

    return redirect('/cobros')

def generar_recibo(request,id_cobro):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="recibo.pdf"'
    Cobro = cobro.objects.get(id_cobro=id_cobro)
    # Crea un archivo PDF
    c = canvas.Canvas(response)

    # Agrega texto al archivo PDF
    c.drawString(100, 730, "SERVICONFI")
    c.drawString(100, 740, "Pedro Francisco Bono No.70      Santiago")
    c.drawString(100, 750, "Nombre: " + Cobro.id_prestamo.id_solicitud.cedula.nombres + Cobro.id_prestamo.id_solicitud.cedula.apellidos)
    c.drawString(100, 760, "Dirección: Calle 123")
    c.drawString(100, 770, "Ciudad: Ciudad de México")

    # Guarda el archivo PDF y lo cierra
    c.save()

    return response

def anulacion_cobros(request, id_cobro):
    Cobro = cobro.objects.get(id_cobro=id_cobro)
    Cobro.estado = 'Anulado'
    Cobro.save()

    return redirect('/cobros')





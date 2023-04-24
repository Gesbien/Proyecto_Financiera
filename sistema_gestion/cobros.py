from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

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
    cont_atrasado = 0
    atrasado = False
    sum_tot = 0
    sum_cap = 0
    sum_int = 0
    tabla = tabla_amortizacion.objects.all().filter(id_prestamo=Prestamo.id_prestamo)

    for item in tabla:
        if Prestamo.balance_actual <= 0:
            Prestamo.estado = 'Pagado'
            Prestamo.save()
            return redirect('/cobros')
        elif Prestamo.tipo_saldo == 'Libre':
            fecha_limite = item.fecha + timedelta(days=Prestamo.dias_gracia)
            if Prestamo.balance_actual <= item.balance_total_esperado:
                item.estado = 'Pagado'
                item.save()
            elif fecha_limite < datetime.strptime('2024-06-27','%Y-%m-%d').date():
                atrasado = True
                cont_atrasado +=1
                cont += 1
                item.estado = 'Atrasado'
                item.save()
                mora = item.cuota * (Prestamo.porciento_mora/100)
                sum_tot += item.cuota
                sum_cap += item.pago_capital
                sum_int += item.pago_interes
            else:
                cont += 1
                item.estado = 'Activo'
                item.save()
        else:
            fecha_limite = item.fecha + timedelta(days=Prestamo.dias_gracia)
            if Prestamo.balance_actual <= item.balance_total_esperado:
                item.estado = 'Pagado'
                item.save()
            elif fecha_limite < datetime.strptime('2023-05-27', '%Y-%m-%d').date():
                atrasado = True
                cont_atrasado += 1
                cont += 1
                item.estado = 'Atrasado'
                item.save()
                mora = item.cuota * (Prestamo.porciento_mora / 100)
                sum_tot += item.cuota
                sum_cap += item.pago_capital
                sum_int += item.pago_interes
            else:
                cont += 1
                item.estado = 'Activo'
                item.save()

    if atrasado == False:
        item = tabla_amortizacion.objects.filter(id_prestamo=Prestamo.id_prestamo).filter(estado='Activo').first()
        sum_tot = item.cuota
        sum_cap = item.pago_capital
        sum_int = item.pago_interes

    Prestamo.cuota_faltantes = cont
    Prestamo.save()

    return round(mora,2),round(sum_tot,2),round(sum_cap,2),round(sum_int,2)

def crear_cobro(request,id_prestamo):
    if cobro.objects.last() is not None:
        Num_cobro = 1 + cobro.objects.last().id_cobro
    else:
        Num_cobro = 1

    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    tabla_amortizada = tabla_amortizacion.objects.all().filter(id_prestamo=id_prestamo)
    fecha_hoy = datetime.today()
    fecha = fecha_hoy.strftime('%Y-%m-%d')
    mora,sum_tot,sum_cap,sum_int = actualizar_prestamo(fecha,Prestamo)
    fecha_convert = fecha_hoy.strftime('%m/%d/%Y')
    monto_total = (Prestamo.balance_actual/Prestamo.cuota_faltantes) + mora
    monto_interes = Prestamo.balance_interes / Prestamo.cuota_faltantes
    monto_capital = monto_total - monto_interes
    context = {
        'num_cobro': Num_cobro,
        'prestamo': Prestamo,
        'tabla'   : tabla_amortizada,
        'fecha'   : fecha_convert,
        'mora'    : mora,
        'total'   : sum_tot,
        'capital' : sum_cap,
        'interes' : sum_int
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

class generar_recibo(View):
    def get(self, request, id):
        Cobro = cobro.objects.get(id_cobro=id)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="recibo.pdf"'

        # Crea un archivo PDF
        c = canvas.Canvas(response)

        # Agrega texto al archivo PDF
        c.drawString(100, 760, "SERVICONFI")
        c.drawString(100, 750, "Pedro Francisco Bono No.70      Santiago")
        c.drawString(100, 740, "Prestamo: " + str(Cobro.id_prestamo.id_prestamo))
        c.drawString(200, 730, "Recibo: " + str(Cobro.id_cobro))
        c.drawString(200, 720, "Fecha: " + str(Cobro.fecha))
        c.drawString(100, 710, "Nombre: " + str(Cobro.id_prestamo.id_solicitud.cedula.nombres) + str(Cobro.id_prestamo.id_solicitud.cedula.apellidos))
        c.drawString(100, 700, "Dirección: " + str(Cobro.id_prestamo.id_solicitud.cedula.direccion))
        c.drawString(100, 690, "Valor de Cuota: " + str(Cobro.monto_total))
        c.drawString(100, 680, "Total de Cuotas Atrasadas: " + str(Cobro.id_prestamo.cuota))
        c.drawString(100, 670, "Capital:  " + str(Cobro.monto_capital))
        c.drawString(100, 660, "Interes:  " + str(Cobro.monto_interes))
        c.drawString(100, 650, "Mora:  " + str(Cobro.monto_mora))
        c.drawString(100, 640, "Total:  " + str(Cobro.monto_total))
        c.drawString(100, 630, "_________________________:  ")
        c.drawString(100, 620, "        Cobrador  ")
        c.drawString(100, 610, " Este recibo es valido solo si esta Firmado")
        # Guarda el archivo PDF y lo cierra
        c.save()

        return response

def anulacion_cobros(request, id_cobro):
    Cobro = cobro.objects.get(id_cobro=id_cobro)
    Cobro.estado = 'Anulado'
    Cobro.save()

    return redirect('/cobros')





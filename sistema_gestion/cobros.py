from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
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
    sum_mora = 0
    cont = 0
    cont_atrasado = 0
    atrasado = False
    tabla = tabla_amortizacion.objects.all().filter(id_prestamo=Prestamo.id_prestamo)
    valor = tabla_amortizacion.objects.filter(id_prestamo=Prestamo).exclude(estado='Pagado').last()
    if Prestamo.tipo_saldo == 'Libre':
        sum_tot = -(valor.cuota - (Prestamo.balance_interes - valor.balance_total_esperado))
        sum_cap = 0
        sum_int = -(valor.pago_interes - (Prestamo.interes_pagado - valor.balance_interes_esperado))
    else:
        sum_tot = -(valor.cuota - (Prestamo.balance_actual - valor.balance_total_esperado))
        sum_cap = -(valor.pago_capital - (Prestamo.capital_pagado - valor.balance_capital_esperado))
        sum_int = -(valor.pago_interes - (Prestamo.interes_pagado - valor.balance_interes_esperado))

    for item in tabla:
        if Prestamo.balance_actual <= 0:
            Prestamo.estado = 'Pagado'
            Prestamo.save()
            return redirect('/cobros')
        elif Prestamo.tipo_saldo == 'Libre':
            fecha_limite = item.fecha + timedelta(days=Prestamo.dias_gracia)
            if Prestamo.balance_interes <= item.balance_total_esperado:
                item.estado = 'Pagado'
                item.save()
            elif fecha_limite < datetime.strptime(fecha_hoy, '%Y-%m-%d').date():
                atrasado = True
                cont_atrasado +=1
                cont += 1
                item.estado = 'Atrasado'
                item.save()
                mora = item.cuota * (Prestamo.porciento_mora/100)
                sum_mora += mora
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
            elif fecha_limite < datetime.strptime(fecha_hoy, '%Y-%m-%d').date():
                atrasado = True
                cont_atrasado += 1
                cont += 1
                item.estado = 'Atrasado'
                item.save()
                mora = item.cuota * (Prestamo.porciento_mora / 100)
                sum_mora += mora
                sum_tot += item.cuota
                sum_cap += item.pago_capital
                sum_int += item.pago_interes
            else:
                cont += 1
                item.estado = 'Activo'
                item.save()
    if atrasado == False:
        item = tabla_amortizacion.objects.filter(id_prestamo=Prestamo.id_prestamo).filter(estado='Activo').first()
        if Prestamo.tipo_saldo == "Libre":
            sum_tot = abs((item.cuota - (Prestamo.balance_interes - (item.balance_total_esperado - item.cuota))))
            sum_cap = item.pago_capital
            sum_int = item.pago_interes - (Prestamo.interes_pagado - (item.balance_interes_esperado - item.pago_interes))
        else:
            if Prestamo.total_pagado == 0:
                sum_tot = item.cuota
            else:
                sum_tot = abs(item.cuota - (Prestamo.balance_actual - (item.balance_total_esperado - item.cuota)))

            if Prestamo.capital_pagado == 0:
                sum_cap = item.pago_capital
            else:
                sum_cap = item.pago_capital - (Prestamo.capital_pagado - (item.balance_capital_esperado - item.pago_capital))

            if Prestamo.interes_pagado == 0:
                sum_int = item.pago_interes
            else:
                sum_int = item.pago_interes - (Prestamo.interes_pagado - (item.balance_interes_esperado - item.pago_interes))


    Prestamo.cuota_faltantes = cont
    Prestamo.save()

    return round(sum_mora,2),round(sum_tot,2),round(sum_cap,2),round(sum_int,2)

def crear_cobro(request,id_prestamo,fecha):
    if cobro.objects.last() is not None:
        Num_cobro = 1 + cobro.objects.last().id_cobro
    else:
        Num_cobro = 1

    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    tabla_amortizada = tabla_amortizacion.objects.all().filter(id_prestamo=id_prestamo)
    if fecha == '0':
        fecha_pos = datetime.today()

    fecha = fecha_pos.strftime('%Y-%m-%d')
    mora,sum_tot,sum_cap,sum_int = actualizar_prestamo(fecha,Prestamo)
    fecha_convert = fecha_pos.strftime('%d/%m/%Y')
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
    fecha = request.POST['datepicker_fecha']
    fecha_exped = datetime.strptime(fecha, '%d-%m-%Y')
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
    Prestamo.total_pagado += Cobro.monto_total
    Prestamo.capital_pagado += Cobro.monto_capital
    Prestamo.interes_pagado += Cobro.monto_interes
    Prestamo.save()

    if Prestamo.tipo_saldo == 'Libre':
        for item in tabla:
            if Prestamo.balance_interes <= item.balance_total_esperado:
                item.estado = 'Pagado'
                item.save()
        if Cobro.monto_capital != 0:
            cuotas = Prestamo.cuota_faltantes
            capital = Prestamo.balance_capital
            tasa_interes = Prestamo.tasa / 100
            monto_interes = round((capital * tasa_interes * cuotas), 2)
            valor_cuota = round(monto_interes / cuotas, 2)
            balance_total = round(monto_interes, 2)

            # Inicialización de variables
            balance_interes = 0
            balance_capital = 0

            interes = monto_interes / cuotas
            capital_cuota = valor_cuota - interes
            Prestamo.monto_interes = monto_interes
            Prestamo.balance_interes = monto_interes
            Prestamo.save()

            for item in tabla:
                balance_total -= valor_cuota
                balance_interes += interes
                item.cuota = valor_cuota
                item.pago_capital = capital_cuota
                item.pago_interes = interes
                item.balance_interes_esperado = balance_interes
                item.balance_capital_esperado += capital_cuota
                item.balance_total_esperado = balance_total
                item.save()
    else:
        for item in tabla:
            if Prestamo.balance_actual <= item.balance_total_esperado:
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
        c.drawString(100, 600, "        Cobrador  ")
        c.drawString(100, 580, " Este recibo es valido solo si esta Firmado")
        # Guarda el archivo PDF y lo cierra
        c.save()

        return response

def anulacion_cobros(request, id_cobro):
    Cobro = cobro.objects.get(id_cobro=id_cobro)
    Cobro.estado = 'Anulado'
    Cobro.save()

    return redirect('/cobros')

def actualizar_datos(request):
    fecha_hoy = request.GET.get('fecha')
    id_prestamo = request.GET.get('id')
    fecha_exped = datetime.strptime(fecha_hoy, '%d-%m-%Y')
    fecha = fecha_exped.strftime('%Y-%m-%d')
    # Aquí puedes realizar las operaciones necesarias para obtener los datos actualizados
    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    mora, sum_tot, sum_cap, sum_int = actualizar_prestamo(fecha, Prestamo)
    total_cuota = sum_tot + mora

    data = {
        'input1_value': mora,
        'input2_value': total_cuota,
        'input3_value': sum_cap,
        'input4_value': sum_int,
    }
    return JsonResponse(data)

def sumatoria_datos(request):
    id_prestamo = request.GET.get('id')
    monto_total = float(request.GET.get('total'))

    monto_mora =  float(request.GET.get('mora'))

    # Aquí puedes realizar las operaciones necesarias para obtener los datos actualizados
    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    Tabla = tabla_amortizacion.objects.filter(id_prestamo=Prestamo).filter(estado='Activo').first()
    total_restante = monto_total - monto_mora
    porcentaje = round((monto_total/Tabla.cuota),2)
    porcentaje_int = round(Tabla.pago_interes/Tabla.cuota,2)
    pago_interes = total_restante * porcentaje_int
    pago_capital = total_restante - pago_interes

    data = {
        'input1_value': monto_mora,
        'input2_value': monto_total,
        'input3_value': pago_capital,
        'input4_value': pago_interes,
    }
    return JsonResponse(data)


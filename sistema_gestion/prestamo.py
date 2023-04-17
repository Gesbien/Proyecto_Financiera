from datetime import datetime,timedelta
from io import BytesIO

from django.template.loader import get_template
from django.views import View

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import prestamo, solicitud, prestamo_garantia, garante, informacion_trabajo, automovil, terreno, marca, modelo, tabla_amortizacion
from .garantia import registroGarantia, edicionGarantia
from .personas import registroPersona, edicionPersona
from xhtml2pdf import pisa

def inicio_prestamo(request):
    prestamos = prestamo.objects.all().exclude(estado='Anulado')
    paginator = Paginator(prestamos, 10)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    solicitudes = solicitud.objects.all().filter(estado='Aceptada')
    context = {
        'solicitudes' : solicitudes,
        'items': items}
    return render(request, 'paginas/gestionPrestamo.html', context)

def crear_prestamo(request,id_solicitud):
    Solicitud = solicitud.objects.get(id_solicitud=id_solicitud)
    if prestamo.objects.last() is not None:
        Num_prestamo = 1 + prestamo.objects.last().id_prestamo
    else:
        Num_prestamo = 1
    Marca = marca.objects.all()
    Modelo = modelo.objects.all()
    context = {
        'opcion'    : 'nv',
        'solicitud' : Solicitud,
        'numero'    : Num_prestamo,
        'marcas': Marca,
        'modelos': Modelo
    }
    return render(request, "paginas/registrarPrestamo.html", context)

def registroPrestamo(request,opcion,id_solicitud,num):
    salida = 'Prestamo'
    monto = float(request.POST['txt_monto'])
    tasa = float(request.POST['txt_tasa'])
    cuota = int(request.POST['txt_cuota'])
    clasificacion = request.POST.get('typeSel')
    tipo_saldo = request.POST.get('typeSaldo')
    porciento_mora = request.POST['txt_%_de_mora']
    dias_gracia = request.POST['txt_dias_de_gracia']
    valor_cuota = request.POST['txt_valor_cuota']
    fecha = request.POST['datepicker-month_inicio']
    fecha_exped = datetime.strptime(fecha, '%m/%d/%Y')
    fecha_convert = fecha_exped.strftime('%Y-%m-%d')
    fecha_tasa = datetime.strptime(fecha_convert, '%Y-%m-%d')
    fecha_fin = request.POST['fecha_fin']
    estado = 'Proceso'
    monto_interes = monto * (tasa / 100) * cuota
    monto_actual = monto + monto_interes

    Solicitud = solicitud.objects.get(id_solicitud=id_solicitud)

    Prestamo = prestamo.objects.create(id_prestamo=num,id_solicitud=Solicitud,fecha_expedicion=fecha_convert,fecha_expiracion=fecha_fin,dias_gracia=dias_gracia,
                                      clasificacion=clasificacion,estado=estado,valor_cuota=valor_cuota,cuota=cuota,tasa=tasa,
                                       monto=monto,porciento_mora=porciento_mora,balance_actual=monto_actual,balance_capital=monto,
                                       balance_interes= monto_interes,cuota_faltantes= cuota,tipo_saldo=tipo_saldo)

    generar_tabla_amortizacion(Prestamo.id_prestamo,fecha_tasa)

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
    elif Prestamo.clasificacion == 'Vehiculo':
        Union_Garantia = prestamo_garantia.objects.get(id_prestamo=id_prestamo)
        Vehiculo = automovil.objects.get(id_garantia=Union_Garantia.id_garantia)
        context = {
            'garantia': Union_Garantia,
            'auto'     : Vehiculo,
            'solicitud': Solicitud,
            'prestamo': Prestamo
        }
    else:
        Union_Garantia = prestamo_garantia.objects.get(id_prestamo=id_prestamo)
        Terreno = terreno.objects.get(id_garantia=Union_Garantia.id_garantia)
        context = {
            'garantia': Union_Garantia,
            'Inmobi': Terreno,
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
    monto_interes = float(monto)*(float(tasa)/100)*int(cuota)
    monto_actual = float(monto) + monto_interes
    tipo_saldo = request.POST.get('typeSaldo')


    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    Prestamo.monto = monto
    Prestamo.tasa = tasa
    Prestamo.cuota = cuota
    Prestamo.cuota_faltantes = cuota
    Prestamo.porciento_mora = porciento_mora
    Prestamo.dias_gracia = dias_gracia
    Prestamo.valor_cuota = valor_cuota
    Prestamo.fecha_expedicion = fecha_convert
    Prestamo.fecha_expiracion = fecha_fin
    Prestamo.balance_capital = monto
    Prestamo.balance_interes = monto_interes
    Prestamo.balance_actual = monto_actual
    Prestamo.tipo_saldo = tipo_saldo
    Prestamo.save()

    tipo = Prestamo.clasificacion
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

def generar_tabla_amortizacion(id_prestamo,fecha):
    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    if(Prestamo.tipo_saldo == 'Absoluto'):
        tabla_amortizacion_absoluta(id_prestamo,Prestamo.cuota,fecha)
    elif(Prestamo.tipo_saldo == 'Insoluto'):
        tabla_amortizacion_insoluta(id_prestamo,Prestamo.monto,Prestamo.tasa,Prestamo.cuota,fecha)

def tabla_amortizacion_absoluta(id_prestamo,cuotas,fecha):
    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    capital = Prestamo.monto
    tasa_interes = Prestamo.tasa/100
    monto_interes = round((capital * tasa_interes * cuotas),2)
    # Cálculo de la cuota
    if(Prestamo.tipo_saldo == 'Absoluto'):
        valor_cuota = round((capital + monto_interes) / cuotas,2)
        balance_total = capital + monto_interes
    else:
        valor_cuota = round(monto_interes/cuotas,2)
        balance_total = round(monto_interes,2)
    estado = 'Activo'

    # Inicialización de variables
    balance_interes = 0
    balance_capital = 0

    interes = monto_interes / cuotas
    capital_cuota = valor_cuota - interes

    # Generación de la tabla de amortización
    for i in range(cuotas):
        # Actualización de los balances
        balance_total -= valor_cuota
        balance_interes += interes
        balance_capital += capital_cuota
        # Actualización de la fecha para el siguiente período
        fecha += timedelta(days=30)
        tabla_amortizacion.objects.create(id_prestamo=id_prestamo, fecha=fecha, cuota=round(valor_cuota,2),
                                          balance_actual=round(balance_total,2), estado=estado,
                                          balance_interes=round(balance_interes,2), balance_capital=round(balance_capital,2))


def tabla_amortizacion_insoluta(id_prestamo,capital, tasa_interes, cuotas,fecha):
    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    # Cálculo de la cuota
    tasa_mensual = tasa_interes/100
    cuota = round((capital * tasa_mensual) / (1 - (1 + tasa_mensual) ** (-cuotas)),2)
    estado = 'Activo'

    # Inicialización de variables
    balance_total = capital
    balance_interes = 0
    balance_capital = 0

    # Generación de la tabla de amortización
    for i in range(cuotas):
        # Cálculo del interés y capital de la cuota
        interes = round(balance_total * tasa_mensual,2)
        capital_cuota = cuota - interes

        # Actualización de los balances
        balance_total -= capital_cuota
        balance_interes += interes
        balance_capital += capital_cuota

        # Actualización de la fecha para el siguiente período
        fecha += timedelta(days=30)
        tabla_amortizacion.objects.create(id_prestamo=Prestamo, fecha=fecha, cuota=round(cuota,2),
                                          balance_actual=round(balance_total,2), estado=estado,
                                          balance_interes=round(balance_interes,2), balance_capital=round(balance_capital,2))

def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

class generar_reporte(View):
    def get(self,request,*args,**kwargs):
        prestamos = prestamo.objects.all()
        template = 'Reportes/ReportePrestamo.html'
        context = {
            'cant' : prestamos.count(),
            'prestamos'  : prestamos
        }
        pdf = render_to_pdf(template,context)
        return HttpResponse(pdf,content_type='application/pdf')

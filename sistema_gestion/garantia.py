from .models import garantia, terreno, automovil,garante,prestamo
from django.shortcuts import render, redirect
from datetime import datetime
def inicio_garantia(request):
    Garantia = garantia.objects.all().exclude(estado='Anulado')
    context = {'garantia': Garantia}
    return render(request, 'paginas/gestionGarantia.html' , context)

def crear_garantia(request):
    Num_Garantia = 1 + garantia.objects.last().id_garantia
    context = {
            'salida' : 'garantia',
            'garantia': Num_Garantia
    }
    return render(request, "paginas/registrarGarantia.html",context)

def registroGarantia(request,salida):
    valor_tasacion = request.POST['txt_valor_tasacion']
    nombre_propetario = request.POST['txt_nombre']
    fecha = request.POST['datepicker-month']
    fecha_exped = datetime.strptime(fecha, '%m/%d/%Y')
    fecha_convert = fecha_exped.strftime('%Y-%m-%d')
    tipo = request.POST.get('roleSel')
    Garantia = garantia.objects.create(valor_tasacion=valor_tasacion,nombre_propetario=nombre_propetario,
                                       estado='Activa',tipo=tipo,fecha_expedicion=fecha_convert)
    if tipo == 'Inmobiliario':
        direccion = request.POST['txt_direccion']
        metraje = request.POST['txt_metraje']
        certificado = request.POST['txt_certificado']
        percela = request.POST['txt_parcela']
        Terreno = terreno.objects.create(id_garantia=Garantia,direccion=direccion,metraje=metraje,
                               certificado_titulo=certificado,numero_parcela=percela)
        if salida == 'garantia':
            return redirect('/garantia')
        else:
            return Terreno

    elif tipo == 'Vehiculo':
        fabricante = request.POST['txt_fabricante']
        modelo = request.POST['txt_modelo']
        anio = request.POST['txt_anio']
        color = request.POST['txt_color']
        placa = request.POST['txt_placa']
        chasis = request.POST['txt_chasis']
        pasajeros = request.POST['txt_pasajeros']
        clasificacion = request.POST['txt_clasificacion']
        Vehiculo = automovil.objects.create(id_garantia=Garantia,fabricante=fabricante,modelo=modelo,anio=anio,color=color,
                                 placa=placa,chasis=chasis,pasajeros=pasajeros,clasificacion=clasificacion)
        if salida == 'garantia':
            return redirect('/garantia')
        else:
            return Vehiculo


def editarGarantia(request,id_garantia):
    Garantia = garantia.objects.get(id_garantia=id_garantia)
    if Garantia.tipo == 'Inmobiliario':
        Inmobi = terreno.objects.get(id_garantia=Garantia)
        context = {
            'Inmobi': Inmobi,
            'salida': 'garantia',
            'garantia': Garantia
        }
    else:
        Vehiculo = automovil.objects.get(id_garantia=Garantia)
        context = {
            'auto': Vehiculo,
            'salida': 'garantia',
            'garantia': Garantia
        }
    return render(request, "paginas/edicionGarantia.html", context)

def edicionGarantia(request,salida,id_garantia):
    valor_tasacion = request.POST['txt_valor_tasacion']
    nombre_propetario = request.POST['txt_nombre']
    fecha = request.POST['datepicker-month']
    fecha_exped = datetime.strptime(fecha, '%d/%m/%Y')
    fecha_convert = fecha_exped.strftime('%Y-%m-%d')
    Garantia = garantia.objects.get(id_garantia=id_garantia)
    Garantia.valor_tasacion = valor_tasacion
    Garantia.nombre_propetario = nombre_propetario
    Garantia.fecha_expedicion = fecha_convert
    Garantia.save()

    if Garantia.tipo == 'Inmobiliario':
        direccion = request.POST['txt_direccion']
        metraje = request.POST['txt_metraje']
        certificado = request.POST['txt_certificado']
        num_parcela = request.POST['txt_parcela']
        Terreno = terreno.objects.get(id_garantia=Garantia)
        Terreno.direccion = direccion
        Terreno.metraje = metraje
        Terreno.certificado_titulo = certificado
        Terreno.numero_parcela = num_parcela
        Terreno.save()
    else:
        fabricante = request.POST['txt_fabricante']
        modelo = request.POST['txt_modelo']
        anio = request.POST['txt_anio']
        color = request.POST['txt_color']
        placa = request.POST['txt_placa']
        chasis = request.POST['txt_chasis']
        pasajeros = request.POST['txt_pasajeros']
        clasificacion = request.POST['txt_clasificacion']
        Automovil = automovil.objects.get(id_garantia=id_garantia)
        Automovil.fabricante = fabricante
        Automovil.modelo = modelo
        Automovil.anio = anio
        Automovil.color = color
        Automovil.placa = placa
        Automovil.chasis = chasis
        Automovil.pasajeros = pasajeros
        Automovil.clasificacion = clasificacion
        Automovil.save()

    if salida == 'garantia':
        return redirect('/garantia')

def anulacionGarantia(request, id_garantia):
    Garantia = garantia.objects.get(id_garantia=id_garantia)
    Garantia.estado = 'Anulado'
    Garantia.save()

    return redirect('/garantia')
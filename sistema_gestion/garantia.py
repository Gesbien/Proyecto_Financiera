from .models import garantia, terreno, automovil,garante,prestamo
from django.shortcuts import render, redirect
from datetime import datetime
def inicio_garantia(request):
    Garantia = garantia.objects.all().exclude(estado='Anulado')
    context = {'garantias': Garantia}
    return render(request, 'paginas/gestionGarantia.html' , context)

def crear_garantia(request):
    Num_Garantia = 1
    context = {
            'salida' : 'garantia',
            'garantia': Num_Garantia
    }
    return render(request, "paginas/registrarGarantia.html",context)

def registroGarantia(request,salida):
    valor_tasacion = request.POST['txt_valor_tasacion']
    nombre_propetario = request.POST['txt_nombre']
    fecha = request.POST['datepicker-month']
    fecha_exped = datetime.strptime(fecha, '%d/%m/%Y')
    fecha_convert = fecha_exped.strftime('%Y-%m-%d')
    tipo = request.POST.get('roleSel')
    Garantia = garantia.objects.create(valor_tasacion=valor_tasacion,nombre_propetario=nombre_propetario,
                                       estado='Activa',tipo=tipo,fecha_expedicion=fecha_convert)
    if tipo == 'Inmobiliario':
        direccion = request.POST['txt_direccion']
        metraje = request.POST['txt_metraje']
        certificado = request.POST['txt_certificado']
        percela = request.POST['txt_parcela']
        terreno.objects.create(id_garantia=Garantia,direccion=direccion,metraje=metraje,
                               certificado_titulo=certificado,numero_parcela=percela)
    elif tipo == 'Vehiculo':
        fabricante = request.POST['txt_fabricante']
        modelo = request.POST['txt_modelo']
        anio = request.POST['txt_anio']
        color = request.POST['txt_color']
        placa = request.POST['txt_placa']
        chasis = request.POST['txt_chasis']
        pasajeros = request.POST['txt_pasajeros']
        clasificacion = request.POST['txt_clasificacion']
        automovil.objects.create(fabricante=fabricante,modelo=modelo,anio=anio,color=color,
                                 placa=placa,chasis=chasis,pasajeros=pasajeros,clasificacion=clasificacion)

    if salida == 'garantia':
        return redirect('/garantia')

def editarGarantia(request,id_garantia):
    Garantia = garantia.objects.get(id_garantia=id_garantia)
    context = {
            'garantia': Garantia
    }
    return render(request,"paginas/edicionGarantia.html",context)

def edicionGarantia(request,salida,id_garantia):
    valor_tasacion = request.POST('txt_valor_tasacion')
    tipo = request.POST.get('dropdown_menu')
    Garantia = garantia.objects.get(id_garantia=id_garantia)
    Garantia.valor_tasacion = valor_tasacion
    Garantia.save()

    if tipo == 'Terreno':
        direccion = request.POST('txt_direccion')
        Terreno = terreno.objects.get(id_garantia=Garantia)
        Terreno.direccion = direccion
        Terreno.save()
    else:
        fabricante = request.POST('txt_fabricante')
        modelo = request.POST('txt_modelo')
        anio = request.POST('txt_anio')
        placa = request.POST('txt_placa')
        chasis = request.POST('txt_chasis')
        Automovil = automovil.objects.get(id_garantia=id_garantia)
        Automovil.fabricante = fabricante
        Automovil.modelo = modelo
        Automovil.anio = anio
        Automovil.placa = placa
        Automovil.chasis = chasis
        Automovil.save()

    if salida == 'garantia':
        redirect('/garantia')

def anulacionGarantia(request, id_garantia):
    Garantia = garantia.objects.get(id_garantia=id_garantia)
    Garantia.estado = 'Anulado'
    Garantia.save()

    return redirect('/garantia')
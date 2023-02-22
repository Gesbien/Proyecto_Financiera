from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import solicitud, persona, informacion_trabajo
from .personas import registroPersona,edicionPersona

def inicio_solicitud(request):
    solicitudes = solicitud.objects.exclude(estado='Aceptada').exclude(estado='Anulado')
    context = {'solicitudes': solicitudes}
    return render(request, 'paginas/gestionSolicitud.html', context)

def crear_solicitud(request,personas):
    Solicitud = 1 + solicitud.objects.last().id_solicitud
    Personas = persona.objects.filter(tipo='Cliente').exclude(estado='Anulado')
    if personas != '0':
        persona_selecionada = persona.objects.get(cedula=personas)
        info_trabj = informacion_trabajo.objects.get(cedula=persona_selecionada)
        context = {'personas'   : Personas,
                   'solicitudes': Solicitud,
                   'persona_seleccion'   : persona_selecionada,
                   'trabajo'    : info_trabj,
                   'opcion'     : 'sl'
                    }
    else:
        context = {'personas'   : Personas,
                   'solicitudes': Solicitud,
                   'persona'    : personas,
                   'opcion'     : 'nv'}

    return render(request, "paginas/registrarSolicitud.html",context)

def registroSolicitud(request,opcion,id_solicitud):
    if opcion == 'sl':
        cedula = request.POST['txt_cedula']
        cedula_sol = persona.objects.get(cedula=cedula)
    else:
        salida = 'solicitud'
        cedula_sol = registroPersona(request,salida)

    monto = request.POST['txt_monto']
    estado = 'Proceso'

    Solicitud = solicitud.objects.create(id_solicitud=id_solicitud,cedula=cedula_sol,monto=monto,estado=estado)

    return redirect('/solicitud')

def editarSolicitud(request,id_solicitud):

    Solicitud = solicitud.objects.get(id_solicitud=id_solicitud)
    info_trabj = informacion_trabajo.objects.get(cedula=Solicitud.cedula)
    Personas = persona.objects.filter(tipo='Cliente').exclude(estado='Anulado')

    context = {
        'personas': Personas,
        'solicitud': Solicitud,
        'trabajo': info_trabj,
    }
    return render(request, "paginas/edicionSolicitud.html", context)

def edicionSolicitud(request,id_solicitud):
    salida = 'sl'
    monto = request.POST['txt_monto']

    edicionPersona(request,salida)

    Solicitud = solicitud.objects.get(id_solicitud=id_solicitud)
    Solicitud.monto = monto
    Solicitud.save()

    return redirect('/solicitud')

def eliminacionSolicitud(request,id_solicitud):
    Solicitud = solicitud.objects.get(id_solicitud=id_solicitud)
    Solicitud.estado = 'Anulado'
    Solicitud.save()

    return redirect('/solicitud')

def procesarSolicitud(request,id_solicitud):
    Solicitud = solicitud.objects.get(id_solicitud=id_solicitud)
    info_trabj = informacion_trabajo.objects.get(cedula=Solicitud.cedula)

    context = {
        'solicitud': Solicitud,
        'trabajo': info_trabj,
    }
    return render(request, "paginas/procesarSolicitud.html", context)

def proceso(request,id_solicitud,eleccion):
    Solicitud = solicitud.objects.get(id_solicitud=id_solicitud)
    Solicitud.estado = eleccion

    if eleccion == 'Aceptada':
        Persona = persona.objects.get(cedula=Solicitud.cedula.cedula)
        Persona.tipo = 'Cliente'
        Persona.save()

    Solicitud.save()

    return redirect('/solicitud')


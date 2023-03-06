from django.shortcuts import render, redirect, get_object_or_404
from .models import persona, informacion_trabajo

def inicio_persona(request):
    Personas = persona.objects.filter(tipo='Cliente').exclude(estado='Anulado')
    context = {'clientes': Personas}
    return render(request, 'paginas/gestionCliente.html' , context)

def crear_persona(request):
    Persona = 1 + persona.objects.last().id_persona
    context = {
            'opcion' : 'cl',
            'cliente': Persona
    }
    return render(request, "paginas/registrarCliente.html",context)

def registroPersona(request,opcion):
        cedula = request.POST['txt_cedula']
        nombres = request.POST["txt_nombres"]
        apellidos = request.POST["txt_apellidos"]
        direccion = request.POST["txt_direccion"]
        telefono = request.POST["txt_telefono"]
        celular = request.POST["txt_celular"]
        estado = 'Activo'

        if opcion == 'solicitud':
            tipo = 'Solicitante'
            Persona = persona.objects.create(cedula=cedula, nombres=nombres,
                                             apellidos=apellidos,
                                             direccion=direccion, telefono=telefono, celular=celular, tipo=tipo,
                                             estado=estado)
            registroInformacion(request, Persona)
            return Persona

        elif opcion == 'Garante':
            tipo = 'Garante'
            Persona = persona.objects.create(cedula=cedula, nombres=nombres,
                                             apellidos=apellidos,
                                             direccion=direccion, telefono=telefono, celular=celular, tipo=tipo,
                                             estado=estado)
            registroInformacion(request,Persona)
            return Persona

        else:
            tipo = 'Cliente'
            Persona = persona.objects.create(cedula=cedula, nombres=nombres,
                                             apellidos=apellidos,
                                             direccion=direccion, telefono=telefono, celular=celular, tipo=tipo,
                                             estado=estado)
            registroInformacion(request, Persona)
            return redirect('/cliente')

def registroInformacion(request,cedula):
    nombre_trabajo = request.POST['txt_trabj_nombre']
    direccion_trabajo = request.POST['txt_trabj_direccion']
    telefono_trabajo = request.POST['txt_trabj_telefono']
    sueldo = request.POST['txt_trabj_sueldo']

    info = informacion_trabajo.objects.create(cedula=cedula,nombre=nombre_trabajo,
                                              telefono=telefono_trabajo,direccion=direccion_trabajo,
                                              sueldo=sueldo)

def editarPersona(request, id_persona):
    Persona = persona.objects.get(id_persona=id_persona)
    info_trabj = informacion_trabajo.objects.get(cedula=Persona)

    data = {
        'opcion' : 'cl',
        'cliente': Persona,
        'trabajo' : info_trabj
    }
    return render(request, "paginas/edicionCliente.html", data)

def edicionPersona(request,salida):
    cedula = request.POST['txt_cedula']
    nombres = request.POST["txt_nombres"]
    apellidos = request.POST["txt_apellidos"]
    direccion = request.POST["txt_direccion"]
    telefono = request.POST["txt_telefono"]
    celular = request.POST["txt_celular"]

    Persona = persona.objects.get(cedula=cedula)
    Persona.cedula = cedula
    Persona.nombres = nombres
    Persona.apellidos = apellidos
    Persona.direccion = direccion
    Persona.telefono = telefono
    Persona.celular = celular
    Persona.save()

    edicionInforme(request,Persona)

    if salida == 'cl':
        return redirect('/cliente')

def edicionInforme(request,cedula):
    nombre_trabajo = request.POST['txt_trabj_nombre']
    telefono_trabajo = request.POST['txt_trabj_telefono']
    direccion_trabajo = request.POST['txt_trabj_direccion']
    sueldo = request.POST['txt_trabj_sueldo']

    Info = informacion_trabajo.objects.get(cedula=cedula)
    Info.nombre = nombre_trabajo
    Info.telefono = telefono_trabajo
    Info.direccion = direccion_trabajo
    Info.sueldo = sueldo
    Info.save()

def anulacionPersona(request, id_persona):
    Persona = persona.objects.get(id_persona=id_persona)
    Persona.estado = 'Anulado'
    Persona.save()

    return redirect('/cliente')

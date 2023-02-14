from django.shortcuts import render, redirect, get_object_or_404
from .models import persona, informacion_trabajo

def inicio_persona(request):
    Personas = persona.objects.all()
    context = {'Personas': Personas}
    return render(request, 'paginas/gestionPersona.html' , context)

def crear_persona(request):
    return render(request, "paginas/gestionPersona.html")

def registroPersona(request,salida):
        cedula = request.POST['txt_cedula']
        nombres = request.POST["txt_nombres"]
        apellidos = request.POST["txt_apellidos"]
        direccion = request.POST["txt_direccion"]
        telefono = request.POST["txt_telefono"]
        celular = request.POST["txt_celular"]
        tipo = 'Solicitante'
        estado = 'Activo'

        Persona = persona.objects.create(cedula=cedula, nombres=nombres,
                                         apellidos=apellidos,
                                         direccion=direccion, telefono=telefono, celular=celular, tipo=tipo, estado=estado)

        registroInformacion(request,Persona)

        if salida == 'Solicitud':
            return Persona
        else:
            redirect('/cliente')

def registroInformacion(request,persona):
    cedula = persona
    nombre_trabajo = request.POST['txt_trabj_nombre']
    telefono_trabajo = request.POST['txt_trabj_direccion']
    direccion_trabajo = request.POST['txt_trabj_telefono']
    sueldo = request.POST['txt_trabj_sueldo']

    info = informacion_trabajo.objects.create(cedula=cedula,nombre=nombre_trabajo,
                                              telefono=telefono_trabajo,direccion=direccion_trabajo,
                                              sueldo=sueldo)

def editarPersona(request, id_persona):
    Persona = persona.objects.get(id_persona=id_persona)
    data = {
        'persona': Persona
    }
    return render(request, "paginas/edicionPersona.html", data)

def edicionPersona(request):
    id_persona = request.POST['txtId_Persona']
    cedula = request.POST['txtCedula']
    nombres = request.POST['txtNombres']
    apellidos = request.POST['txtApellidos']
    direccion = request.POST['txtDireccion']
    telefono = request.POST['txtTelefono']
    celular = request.POST['txtcelular']
    tipo = request.POST['txtTipo']
    estado = request.POST['txtEstado']


    Persona = persona.objects.get(id_persona=id_persona)
    Persona.cedula = cedula
    Persona.nombres = nombres
    Persona.apellidos = apellidos
    Persona.direccion = direccion
    Persona.telefono = telefono
    Persona.celular = celular
    Persona.tipo = tipo
    Persona.estado = estado
    Persona.save()

    return redirect('/cliente')

def eliminacionPersona(request, id_persona):
    Persona = persona.objects.get(id_persona=id_persona)
    Persona.estado = 'Anulado'
    Persona.save()

    return redirect('/persona')

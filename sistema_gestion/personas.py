from django.shortcuts import render, redirect, get_object_or_404
from .models import persona

def inicio_persona(request):
    Personas = persona.objects.all()
    context = {'Personas': Personas}
    return render(request, 'paginas/gestionPersona.html' , context)

def crear_persona(request):
    return render(request, "paginas/gestionPersona.html")

def registroPersona(request):
    id_persona = request.POST['txtId_Persona']
    cedula = request.POST['txtCedula']
    nombres = request.POST['txtNombres']
    apellidos = request.POST['txtApellidos']
    direccion = request.POST['txtDireccion']
    telefono = request.POST['txtTelefono']
    celular = request.POST['txtcelular']
    tipo = request.POST['txtTipo']
    estado = request.POST['txtEstado']

    Persona = persona.objects.create(id_persona=id_persona, cedula=cedula, nombres=nombres,
                                     apellidos=apellidos,
                                     direccion=direccion, telefono=telefono, celular=celular, tipo=tipo, estado=estado)
    return redirect('/persona')

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

    return redirect('/persona')

def eliminacionPersona(request, id_persona):
    Persona = persona.objects.get(id_persona=id_persona)
    Persona.estado = 'Anulado'
    Persona.save()

    return redirect('/persona')

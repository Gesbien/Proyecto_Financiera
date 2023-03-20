from .models import empleados,persona, informacion_trabajo
from .personas import registroPersona, edicionPersona
from django.shortcuts import render, redirect
from datetime import datetime

def inicio_empleados(request):
    Empleado = empleados.objects.all()
    context = {'empleados': Empleado}
    return render(request, 'paginas/gestionEmpleados.html' , context)

def crear_empleado(request):
    if empleados.objects.last() is not None:
        Empleado = 1 + empleados.objects.last().id
    else:
        Empleado = 1
    context = {
         'Empleado': Empleado,
         'opcion': 'Empleado'
    }
    return render(request, "paginas/registrarEmpleados.html", context)

def registroEmpleados(request,salida):
    Cedula = registroPersona(request,salida)
    sueldo = request.POST['txt_sueldo']
    usuario = request.POST['txt_usuario']
    password = request.POST['txt_password']
    estado = 'activo'
    rol = request.POST['txt_rol']


    Empleado = empleados.objects.create(cedula= Cedula, sueldo=sueldo, estado=estado,
                                           password=password,
                                           usuario=usuario, rol=rol)

    return redirect('/empleados')


def editarEmpleado(request,id_empleado):
    Empleado = empleados.objects.get(id=id_empleado)
    data = {
        'Empleado': Empleado,
    }
    return render(request, "paginas/edicionEmpleados.html", data)

def edicionEmpleados(request,id_empleado):
    salida = 'sl'
    sueldo = request.POST['txt_sueldo']
    usuario = request.POST['txt_usuario']
    password = request.POST['txt_password']
    rol = request.POST['txt_rol']
    edicionPersona(request, salida)


    Empleado = empleados.objects.get(id=id_empleado)
    Empleado.sueldo = sueldo
    Empleado.usuario = usuario
    Empleado.password = password
    Empleado.rol = rol
    Empleado.save()
    return redirect('/empleados')

def anulacionEmpleado(request,id_empleado):
    Empleado = empleados.objects.get(id=id_empleado)
    Empleado.estado = 'Anulado'
    Empleado.save()

    return redirect('/empleados')
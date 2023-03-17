from .models import empleados,persona, informacion_trabajo
from .personas import registroPersona, edicionPersona
from django.shortcuts import render, redirect
from datetime import datetime

def inicio_empleados(request):
    Empleado = empleados.objects.all()
    context = {'empleado': Empleado}
    return render(request, 'paginas/gestionEmpleados.html' , context)

def crear_empleado(request):
    if empleados.objects.last() is not None:
        Empleado = 1 + empleados.objects.last().id
    else:
        Empleado = 1
    context = {
         'Empleado': Empleado,
         'opcion': 'Em'
    }
    return render(request, "paginas/registrarEmpleado.html", context)

def registroEmpleados(request,salida):
    Cedula = registroPersona(request,salida)
    sueldo = request.POST['txt_Sueldo']
    usuario = request.POST['txt_usuario']
    password = request.POST['txt_password']
    estado = 'activo'
    rol = request.POST['txt_rol']
    Cedula.tipo = 'empleado'
    Cedula.save()

    Empleado = empleados.objects.create(cedula= Cedula, sueldo=sueldo, estado=estado,
                                           password=password,
                                           usuario=usuario, rol=rol)

    return redirect('/empleado')


def editarEmpleado(request,id_empleado):
    Empleado = empleados.objects.get(id=id_empleado)
    info_trabj = informacion_trabajo.objects.get(cedula=Empleado.cedula)
    data = {
        'Empleado': Empleado,
        'trabajo': info_trabj
    }
    return render(request, "paginas/edicionEmpleado.html", data)

def edicionEmpleados(request,id_empleado):
    salida = 'sl'
    sueldo = request.POST['txt_Sueldo']
    usuario = request.POST['txt_usuario']
    password = request.POST['txt_password']
    rol = request.POST['txt_rol']
    estado = 'activo'
    edicionPersona(request, salida)


    Empleado = empleados.objects.get(id=id_empleado)
    Empleado.sueldo = sueldo
    Empleado.usuario = usuario
    Empleado.password = password
    Empleado.estado = estado
    Empleado.rol = rol
    Empleado.save()
    return redirect('/empleado')

def anulacionEmpleado(request,id_empleado):
    Empleado = empleados.objects.get(id=id_empleado)
    Empleado.estado = 'Anulado'
    Empleado.save()

    return redirect('/empleado')
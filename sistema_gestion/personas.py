from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from io import BytesIO

from .models import persona, informacion_trabajo, prestamo, garante,garantia,cobro, prestamo_garantia

def inicio_persona(request):
    Personas = persona.objects.filter(tipo='Cliente').exclude(estado='Anulado')
    paginator = Paginator(Personas, 10)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    context = {
        'clientes': Personas,
        'items' : items
    }
    return render(request, 'paginas/gestionCliente.html' , context)
def vista_cliente(request,cedula):
    cliente = persona.objects.get(cedula=cedula)
    prestamos = prestamo.objects.all().filter(id_solicitud__cedula=cliente)
    cobros = cobro.objects.all().filter(id_prestamo__id_solicitud__cedula=cliente)
    union = prestamo_garantia.objects.all().filter(id_prestamo__id_solicitud__cedula=cliente)
    garantes = garante.objects.all().filter(id_prestamo__id_solicitud__cedula=cliente)
    context = {
            'prestamos' : prestamos,
            'cobros'    : cobros,
            'union'     : union,
            'garantes'  : garantes,
            'cliente'   : cliente
    }
    return render(request, "paginas/VistaClientes.html",context)

def crear_persona(request):
    if persona.objects.last() is not None:
        Persona = 1 + persona.objects.last().id_persona
    else:
        Persona = 1
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

        elif opcion == 'Empleado':
            tipo = 'Empleado'
            Persona = persona.objects.create(cedula=cedula, nombres=nombres,
                                             apellidos=apellidos,
                                             direccion=direccion, telefono=telefono, celular=celular, tipo=tipo,
                                             estado=estado)
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
        edicionInforme(request,Persona)
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
        clientes = persona.objects.all().filter(tipo='Cliente')
        template = 'Reportes/ReporteCliente.html'
        context = {
            'cant' : clientes.count(),
            'clientes'  : clientes
        }
        pdf = render_to_pdf(template,context)
        return HttpResponse(pdf,content_type='application/pdf')
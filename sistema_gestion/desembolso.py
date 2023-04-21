from io import BytesIO
from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import  ListView, CreateView
from django.template.loader import get_template
from django.views import View

from .models import desembolso,prestamo, persona, solicitud
from .personas import registroPersona
from xhtml2pdf import pisa

def inicio_desmbolso(request):
    Desembolso = desembolso.objects.all()
    paginator = Paginator(Desembolso, 10)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    context = {'items': items}
    return render(request, 'paginas/gestionDesembolso.html', context)

def crear_desembolso(request,id_prestamo):
    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    Solicitud = solicitud.objects.get(id_solicitud=Prestamo.id_solicitud.id_solicitud)
    Persona = persona.objects.get(cedula=Solicitud.cedula.cedula)
    if desembolso.objects.last() is not None:
        Num_desembolso = 1 + desembolso.objects.last().id_desembolso
    else:
        Num_desembolso = 1
    context = {
            'prestamo' : Prestamo,
            'cliente'  : Persona,
            'numero'   : Num_desembolso
    }
    return render(request, "paginas/registrarDesembolso.html", context)

def registroDesembolso(request,id_prestamo):
    Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    monto = request.POST['txt_Monto']
    codigo_cuenta_cheque = request.POST['txt_num']
    fecha = request.POST['datepicker-month_inicio']
    fecha_exped = datetime.strptime(fecha, '%m/%d/%Y')
    fecha_convert = fecha_exped.strftime('%Y-%m-%d')
    concepto = request.POST['txt_Concepto']
    estado = 'Activo'
    orden_de = request.POST['txt_Nombres']
    tipo = request.POST['txt_tipo']

    Prestamo.estado = 'Desembolsado'
    Prestamo.save()


    Desembolso = desembolso.objects.create( id_prestamo = Prestamo  ,monto_total=monto,estado=estado,codigo_cuenta_cheque=codigo_cuenta_cheque,
                                            fecha = fecha_convert, nombre_cliente= orden_de, tipo = tipo, concepto=concepto )

    return redirect('/prestamo')

def editarDesembolso(request, id_desembolso):
    Desembolso = desembolso.objects.get(id_desembolso=id_desembolso)
    data = {
        'desembolso': Desembolso
    }
    return render(request, "paginas/edicionDesembolso.html", data)

def edicionDesembolso(request):
    id_solicitud = request.POST['txtId_Solicitud']
    id_prestamo = request.POST['txtId_Prestamo']
    estado = request.POST['txtEstado']
    monto_total = request.POST['numMonto']
    codigo_cuenta_cheque = request.POST['txt_num']
    fecha = request.POST['datepicker-month_inicio']
    fecha_exped = datetime.strptime(fecha, '%m/%d/%Y')
    fecha_convert = fecha_exped.strftime('%Y-%m-%d')
    orden_de = request.POST['txt_Nombres']
    tipo = request.POST['txt_tipo']

    Desembolso = desembolso.objects.get(id_solicitud=id_solicitud)
    Desembolso.id_prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
    Desembolso.codigo_cuenta_cheque = codigo_cuenta_cheque
    Desembolso.estado = estado
    Desembolso.monto = monto_total
    Desembolso.fecha = fecha_convert
    Desembolso.nombre_cliente = orden_de
    Desembolso.tipo = tipo
    Desembolso.save()

    return redirect('/prestamo')

def eliminacionDesembolso(request, id_desembolso):
    Desembolso = desembolso.objects.get(id_desembolso=id_desembolso)
    Desembolso.estado = 'Anulado'
    Desembolso.save()
    Prestamo = prestamo.objects.get(id_prestamo=Desembolso.id_prestamo.id_prestamo)

    Prestamo.estado = 'Proceso'
    Prestamo.save()



    return redirect('/desembolso')

def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

class generar_reporte(View):
    def post(self, request):
        fecha_inicio = request.POST['datepicker_monthi']
        fecha_expedi = datetime.strptime(fecha_inicio, '%m/%d/%Y')
        fecha_converti = fecha_expedi.strftime('%Y-%m-%d')
        fecha_final = request.POST['datepicker_monthf']
        fecha_expedf = datetime.strptime(fecha_final, '%m/%d/%Y')
        fecha_convertf = fecha_expedf.strftime('%Y-%m-%d')

        desembolsos = desembolso.objects.filter(fecha__gte=fecha_converti,fecha__lte=fecha_convertf)
        template = 'Reportes/ReporteDesembolso.html'
        context = {
           'cant': desembolsos.count(),
            'desembolsos': desembolsos
        }
        pdf = render_to_pdf(template, context)
        return HttpResponse(pdf, content_type='application/pdf')
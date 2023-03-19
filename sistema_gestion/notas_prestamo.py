from datetime import datetime
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import prestamo, notas


def inicio_notas(request):
    notas_prestamo = notas.objects.all().exclude(estado='Anulado')
    context = {
        'notas_prestamo' : notas_prestamo,
        }
    return render(request, 'paginas/gestionNotas.html', context)

def crear_notas(request,id_prestamo):
    if notas.objects.last() is not None:
        Num_nota = 1 + notas.objects.last().id_nota
    else:
        Num_nota = 1
    Prestamos = prestamo.objects.all().filter(estado='Desembolsado')
    paginator = Paginator(Prestamos, 5)
    page = request.GET.get('page')
    items = paginator.get_page(page)

    if id_prestamo != '0':
        Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
        context = {
            'items': items,
            'num_nota': Num_nota,
            'prestamo' : Prestamo
        }
    else:
        context = {
            'items' : items,
            'num_nota'  : Num_nota
        }
    return render(request, "paginas/registrarNotas.html", context)

def registro_notas(request,id_nota):
    id_prestamo = request.POST['txt_prestamos']
    tipo = request.POST['drop_tipo']
    monto_total = request.POST['txt_monto_total']
    monto_interes = request.POST['txt_monto_interes']
    monto_capital = request.POST['txt_monto_capital']
    fecha = request.POST['txt_fecha']
    fecha_exped = datetime.strptime(fecha, '%m/%d/%Y')
    fecha_convert = fecha_exped.strftime('%Y-%m-%d')
    estado = 'Realizada'

    if tipo == 'Credito':
        Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
        Prestamo.balance_actual -= monto_total
        Prestamo.balance_capital -= monto_capital
        Prestamo.balance_interes -= monto_interes
    else:
        Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
        Prestamo.balance_actual += monto_total
        Prestamo.balance_capital += monto_capital
        Prestamo.balance_interes += monto_interes

    notas.objects.create(id_nota=id_nota,tipo=tipo,monto_total=monto_total,monto_interes=monto_interes,
                         monto_capital=monto_capital,fecha=fecha_convert,estado=estado,
                         id_prestamo=Prestamo)

    return redirect('/notas')

def anulacion_notas(request, id_nota):
    Nota = notas.objects.get(id_nota=id_nota)
    Nota.estado = 'Anulado'
    Nota.save()

    Prestamo = Nota.id_prestamo
    if Nota.tipo == 'Credito':
        Prestamo.balance_actual += Nota.monto_total
        Prestamo.balance_capital += Nota.monto_capital
        Prestamo.balance_interes += Nota.monto_interes
    else:
        Prestamo.balance_actual -= Nota.monto_total
        Prestamo.balance_capital -= Nota.monto_capital
        Prestamo.balance_interes -= Nota.monto_interes


    return redirect('/notas')
from datetime import datetime
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import prestamo, cobro

def inicio_cobros(request):
    Cobros = cobro.objects.all().exclude(estado='Anulado')
    context = {'cobros': Cobros}
    return render(request, 'paginas/gestionCobro.html', context)

def crear_cobro(request,id_prestamo):
    if cobro.objects.last() is not None:
        Num_cobro = 1 + cobro.objects.last().id_nota
    else:
        Num_cobro = 1
    Prestamos = prestamo.objects.all().filter(estado='Desembolsado')
    paginator = Paginator(Prestamos, 5)
    page = request.GET.get('page')
    items = paginator.get_page(page)

    if id_prestamo != '0':
        Prestamo = prestamo.objects.get(id_prestamo=id_prestamo)
        context = {
            'items': items,
            'num_cobro': Num_cobro,
            'prestamo': Prestamo
        }
    else:
        context = {
            'items': items,
            'num_nota': Num_cobro
        }
    return render(request, "paginas/registrarPrestamo.html", context)
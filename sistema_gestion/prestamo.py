from django.shortcuts import render, redirect
from .models import prestamo

def inicio_prestamo(request):
    prestamos = prestamo.objects.all()
    context = {'prestamo': prestamos}
    return render(request, 'paginas/gestionPrestamo.html', context)
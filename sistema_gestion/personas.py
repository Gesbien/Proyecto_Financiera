from django.shortcuts import render, redirect
from .models import persona

# Create your views here.

def index(request):
    personas = persona.objects.all()
    context = {'persona': personas}
    return render(request, 'paginas/persona.html', context)

def create(request):
    personas = persona(cedula=request.POST.get('cedula'), nombres=request.POST.get('nombre'),primer_apellido=request.POST.get('primer_apellido'),estado='Activo')
    personas.save()
    return redirect('crear')

def edit(request, id):
    personas = persona.objects.get(id_persona=id)
    context = {'persona': personas}
    return render(request, 'paginas/edit.html', context)

def update(request, id):
    personas = persona.objects.get(id=id)
    personas.cedula = request.POST['cedula']
    personas.nombres = request.POST['nombre']
    personas.primer_apellido = request.POST['primer_apellido']
    personas.save()
    return redirect('/paginas/')

def delete(request, id):
    personas = persona.objects.get(id_persona=id)
    personas.estado = 'Anulado'
    return redirect('/paginas/')
from django.shortcuts import render
from django.http import HttpResponse
from .models import solicitud
# Create your views here.

def inicio(request):
     return HttpResponse("<h1>Bienvenido al Sistema</h1>")
def personas(request):
     return render(request,'paginas/persona.html')

def home (request):
     solicitudListados = solicitud.objects.all()
     return render(request, "gestionSolicitud.html",{"solicitudes":solicitudListados})

def registrarSolicitud(request):
     id_solicitud = request.POST['txtId_Solicitud']
     id_persona = request.POST['txtId_Persona']
     estado = request.POST['txtEstado']
     monto = request.POST['numMonto']
     tasa = request.POST['numTasa']
     cuota = request.POST['numCuota']

     Solicitud = solicitud.objects.create(id_solicitud=id_solicitud, id_persona=id_persona,estado=estado,monto=monto,tasa=tasa,cuota=cuota)
     return redirect('/')

def edicionSolicitud(request,id_solicitud):
     Solicitud = solicitud.objects.get(id_solicitud=id_solicitud)
     return render(request,"edicionSolicitud.html", {"solicitud":solicitud})

def editarSolicitud(request):
     id_solicitud = request.POST['txtId_Solicitud']
     id_persona = request.POST['txtId_Persona']
     estado = request.POST['txtEstado']
     monto = request.POST['numMonto']
     tasa = request.POST['numTasa']
     cuota = request.POST['numCuota']

     Solicitud = solicitud.objects.get(id_solicitud=id_solicitud)
     Solicitud.id_persona = id_persona
     Solicitud.estado = estado
     Solicitud.monto = monto
     Solicitud.tasa = tasa
     Solicitud.cuota = cuota
     Solicitud.save()

     return redirect('/')

def eliminacionSolicitud(request,id_solicitud):
     Solicitud = solicitud.objects.get(id_solicitud=id_solicitud)
     Solicitud.delete()

     return redirect('/')
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import solicitud
from .models import empleados
# Create your views here.

def inicio(request):
     return render(request,'paginas/index.html')

def login(request):
     if request.method == 'POST':
          usuario = request.POST['txt_usuario']
          contrasena = request.POST['txt_password']
          try:
               user = empleados.empAuth.get(usuario=usuario,password=contrasena)
               if user is not None:
                    return render(request,'paginas/index.html')
               else:
                    context = {
                         "err" : 'Usuario Invalido o Contraseña Invalidad'
                    }
                    return render(request,'accounts/login.html', context)
          except Exception as identifier:
               return redirect('/')
     else:
          return render(request,'accounts/login.html')

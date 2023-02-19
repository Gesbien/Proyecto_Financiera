from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import solicitud
from .models import persona
# Create your views here.

def inicio(request):
     return render(request,'paginas/index.html')
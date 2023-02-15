from django.urls import path
from django.contrib import admin
from . import views
from . import personas
from . import solicitud, prestamo

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('solicitud', solicitud.inicio_solicitud, name='inicio_solicitud'),
    path('solicitud/registrar/<personas>', solicitud.crear_solicitud, name='registrarSolicitud'),
    path('solicitud/registro/<opcion>', solicitud.registroSolicitud, name='registroSolicitud'),
    path('solicitud/editar/<id_solicitud>', solicitud.editarSolicitud, name='editarSolicitud'),
    path('solicitud/edicion/<id_solicitud>', solicitud.edicionSolicitud, name='edicionSolicitud'),
    path('solicitud/anular/<id_solicitud>', solicitud.eliminacionSolicitud, name='anularSolicitud'),
    path('prestamo',prestamo.inicio_prestamo,name='inicio_persona')

]
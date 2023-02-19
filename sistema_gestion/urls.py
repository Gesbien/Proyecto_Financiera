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
    path('solicitud/procesar/<id_solicitud>',solicitud.procesarSolicitud, name='procesarSolicitud'),
    path('solicitud/procesado/<id_solicitud>/<eleccion>',solicitud.proceso,name='procesoSolicitud'),
    path('prestamo',prestamo.inicio_prestamo,name='inicio_prestamo'),
    path('cliente', personas.inicio_persona, name='inicio_cliente'),
    path('cliente/registrar', personas.crear_persona,name='crear_cliente'),
    path('ciente/registro',personas.registroPersona,name='registro_cliente'),
    path('cliente/editar/<id_persona>', personas.editarPersona, name='editarCliente'),
    path('cliente/edicion/<id_persona>', personas.edicionPersona, name='edicionCliente'),

]
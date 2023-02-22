from django.urls import path
from django.contrib import admin
from . import views
from . import personas
from . import solicitud, prestamo

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('solicitud', solicitud.inicio_solicitud, name='inicio_solicitud'),
    path('solicitud/registrar/<personas>', solicitud.crear_solicitud, name='registrarSolicitud'),
    path('solicitud/registro/<opcion>/<id_solicitud>', solicitud.registroSolicitud, name='registroSolicitud'),
    path('solicitud/editar/<id_solicitud>', solicitud.editarSolicitud, name='editarSolicitud'),
    path('solicitud/edicion/<id_solicitud>', solicitud.edicionSolicitud, name='edicionSolicitud'),
    path('solicitud/anular/<id_solicitud>', solicitud.eliminacionSolicitud, name='anularSolicitud'),
    path('solicitud/procesar/<id_solicitud>',solicitud.procesarSolicitud, name='procesarSolicitud'),
    path('solicitud/procesado/<id_solicitud>/<eleccion>',solicitud.proceso,name='procesoSolicitud'),
    path('cliente', personas.inicio_persona, name='inicio_cliente'),
    path('cliente/registrar', personas.crear_persona,name='crear_cliente'),
    path('cliente/registro/<opcion>',personas.registroPersona,name='registro_cliente'),
    path('cliente/editar/<id_persona>', personas.editarPersona, name='editarCliente'),
    path('cliente/edicion/<salida>', personas.edicionPersona, name='edicionCliente'),
    path('cliente/anular/<id_persona>',personas.anulacionPersona, name='anulacionCliente'),
    path('prestamo', prestamo.inicio_prestamo, name='inicio_prestamo'),

]
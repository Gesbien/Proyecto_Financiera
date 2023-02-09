from django.urls import path
from django.contrib import admin
from . import views
from . import personas
from . import solicitud

urlpatterns = [
    path('admin/',admin.site.urls),
    path('',views.inicio,name='inicio'),
    path('personas',solicitud.inicio_solicitud,name='inicio_solicitud'),
    path('personas/crear',personas.create,name='crear'),
    path('personas/editar',personas.edit,name='editar'),
    path('personas/eliminar',personas.delete,name='eliminar'),
    path('registrarSolicitud/',solicitud.crear_solicitud,name='registrarSolicitud'),
    path('registroSolicitud/',solicitud.registroSolicitud,name='registroSolicitud'),
    path('edicionSolicitud/<id_solicitud>',views.edicionSolicitud),
    path('editarSolicitud/',views.editarSolicitud),
    path('eliminacionSolicitud/',views.eliminacionSolicitud)

]
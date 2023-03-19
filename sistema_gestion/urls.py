from django.urls import path
from django.contrib import admin
from . import views, solicitud, prestamo, garantia, personas, desembolso, empleados, notas_prestamo


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
    path('prestamo/registrar/<id_solicitud>', prestamo.crear_prestamo, name='registroPrestamo'),
    path('prestamo/registro/<opcion>/<id_solicitud>',prestamo.registroPrestamo,name='registro_prestamo'),
    path('prestamo/editar/<id_prestamo>', prestamo.editarPrestamo, name='editarPrestamo'),
    path('prestamo/edicion/<id_prestamo>', prestamo.edicionPrestamo, name='edicionPrestamo'),
    path('prestamo/anular/<id_prestamo>',prestamo.anulacionPrestamo,name='anular_prestamo'),
    path('garantia',garantia.inicio_garantia,name='inicio_garantia'),
    path('garantia/registrar',garantia.crear_garantia,name='registrar_garantia'),
    path('garantia/registro/<salida>',garantia.registroGarantia,name='registro_garantia'),
    path('garantia/editar/<id_garantia>',garantia.editarGarantia,name='editar_garantia'),
    path('garantia/edicion/<salida>/<id_garantia>',garantia.edicionGarantia, name='edicion_garantia'),
    path('garantia/anular/<id_garantia>',garantia.anulacionGarantia,name='anular_garantia'),
    path('desembolso',desembolso.inicio_desmbolso,name='inicio_desembolso'),
    path('desembolso/registrar/<id_prestamo>',desembolso.crear_desembolso,name='inicio_desembolso'),
    path('desembolso/registro/<id_prestamo>',desembolso.registroDesembolso, name='registro_desembolso'),
    path('desembolso/anular/<id_desembolso>',desembolso.eliminacionDesembolso, name='eliminacionDesembolso'),
    path('empleados', empleados.inicio_empleados, name='inicio_empleado'),
    path('empleados/registrar', empleados.crear_empleado,name='crear_empleado'),
    path('empleado/registro/<salida>', empleados.registroEmpleados, name='registro_empleado'),
    path('empleado/editar/<id_empleado>', empleados.editarEmpleado, name='edicionEmpleado'),
    path('empleado/edicion/<id_empleado>', empleados.editarEmpleado, name='edicionEmpleado'),
    path('empleado/anular/<id_empleado>',empleados.anulacionEmpleado, name='anulacionEmpleado'),
    path('notas',notas_prestamo.inicio_notas, name='inicio_notas'),
    path('notas/registrar/<id_prestamo>', notas_prestamo.crear_notas,name='registrar_notas'),
    path('notas/registro/<id_prestamo>',notas_prestamo.registro_notas,name='registro_notas'),
    path('notas/anular/<id_nota>',notas_prestamo.anulacion_notas,name='anular_notas')


]
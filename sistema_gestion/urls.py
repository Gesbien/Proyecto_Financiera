from django.urls import path
from django.contrib import admin

import sistema_gestion.cobros
from . import views, solicitud, prestamo, garantia, personas, desembolso, empleados, cobros, notas_prestamo


urlpatterns = [
    path('', views.login, name="login"),
    path('inicio', views.inicio, name='inicio'),
    path('solicitud', solicitud.inicio_solicitud, name='inicio_solicitud'),
    path('solicitud/reporte', solicitud.generar_reporte.as_view(), name='reporte_solicitud'),
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
    path('prestamo/reporte', prestamo.generar_reporte.as_view(), name='reporte_prestamo'),
    path('prestamo/registrar/<id_solicitud>', prestamo.crear_prestamo, name='registroPrestamo'),
    path('prestamo/registro/<opcion>/<id_solicitud>/<num>',prestamo.registroPrestamo,name='registro_prestamo'),
    path('prestamo/editar/<id_prestamo>', prestamo.editarPrestamo, name='editarPrestamo'),
    path('prestamo/edicion/<id_prestamo>', prestamo.edicionPrestamo, name='edicionPrestamo'),
    path('prestamo/anular/<id_prestamo>',prestamo.anulacionPrestamo,name='anular_prestamo'),
    path('garantia',garantia.inicio_garantia,name='inicio_garantia'),
    path('garantia/reporte', garantia.generar_reporte.as_view(), name='reporte_garantia'),
    path('garantia/registrar',garantia.crear_garantia,name='registrar_garantia'),
    path('garantia/registro/<salida>',garantia.registroGarantia,name='registro_garantia'),
    path('garantia/editar/<id_garantia>',garantia.editarGarantia,name='editar_garantia'),
    path('garantia/edicion/<salida>/<id_garantia>',garantia.edicionGarantia, name='edicion_garantia'),
    path('garantia/anular/<id_garantia>',garantia.anulacionGarantia,name='anular_garantia'),
    path('desembolso',desembolso.inicio_desmbolso,name='inicio_desembolso'),
    path('desembolso/reporte', desembolso.generar_reporte.as_view(), name='reporte_desembolso'),
    path('desembolso/registrar/<id_prestamo>',desembolso.crear_desembolso,name='inicio_desembolso'),
    path('desembolso/registro/<id_prestamo>',desembolso.registroDesembolso, name='registro_desembolso'),
    path('desembolso/editar/<id_desembolso>', desembolso.editarDesembolso, name='edicionDesembolso'),
    path('desembolso/anular/<id_desembolso>',desembolso.eliminacionDesembolso, name='eliminacionDesembolso'),
    path('empleados', empleados.inicio_empleados, name='inicio_empleado'),
    path('empleados/registrar', empleados.crear_empleado,name='crear_empleado'),
    path('empleados/registro/<salida>', empleados.registroEmpleados, name='registro_empleado'),
    path('empleados/editar/<id_empleado>', empleados.editarEmpleado, name='edicionEmpleado'),
    path('empleados/edicion/<id_empleado>', empleados.edicionEmpleados, name='edicionEmpleado'),
    path('empleados/anular/<id_empleado>',empleados.anulacionEmpleado, name='anulacionEmpleado'),
    path('cobros/',cobros.inicio_cobros, name='inicio_cobro'),
    path('cobros/recibo/<int:id>',cobros.generar_recibo.as_view(),name='recibo'),
    path('cobros/registrar/<id_prestamo>', cobros.crear_cobro, name='registrar_cobro'),
    path('cobros/registro/<id_cobro>', cobros.registro_cobros, name='registro_cobro'),
    path('cobros/editar/<id_cobro>', cobros.editar_cobro, name='editar_cobro'),
    path('cobros/edicion/<id_cobro>', cobros.edicion_cobros, name='edicion_cobro'),
    path('cobros/postear/<id_cobro>',cobros.postear_cobros, name='postear_cobro'),
    path('cobros/anular/<id_cobro>', cobros.anulacion_cobros, name='anulacion_cobros'),
    path('notas', notas_prestamo.inicio_notas, name='inicio_notas'),
    path('notas/registrar/<id_prestamo>', notas_prestamo.crear_notas, name='registrar_notas'),
    path('notas/registro/<id_nota>', notas_prestamo.registro_notas, name='registro_notas'),
    path('notas/postear/<id_nota>', notas_prestamo.postear_notas, name='postear_notas'),
    path('notas/anular/<id_nota>', notas_prestamo.anulacion_notas, name='anular_notas'),

]
from django.contrib import admin
from sistema_gestion.models import solicitud,persona,informacion

# Register your models here.
admin.site.register(solicitud)
admin.site.register(persona)
admin.site.register(informacion)
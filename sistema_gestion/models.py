from django.db import models

# Create your models here.
class persona(models.Model):
    id_persona = models.IntegerField(primary_key= True)
    cedula = models.IntegerField(unique= True)
    nombres = models.CharField(max_length= 80,unique=True)
    primer_apellido = models.CharField(max_length=40)
    segundo_apellido = models.CharField(max_length=40)
    tipo = models.CharField(max_length=40)
    estado = models.CharField(max_length=40)

    def __str__(self):
        return self.id_persona

class informacion(models.Model):
    id_informacion = models.IntegerField(primary_key= True)
    id_persona = models.IntegerField(unique= True)
    tipo = models.CharField(max_length= 40)
    descripcion = models.CharField(max_length = 128)
    estado = models.CharField(max_length=40)

    def __str__(self):
        return self.id_informacion
class solicitud(models.Model):
    id_solicitud = models.IntegerField(primary_key = True)
    id_persona = models.IntegerField()
    estado = models.CharField(max_length= 40)
    monto = models.FloatField()
    tasa = models.FloatField()
    cuota = models.IntegerField()
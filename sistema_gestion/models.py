from django.db import models


# Create your models here.
class persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    cedula = models.IntegerField(unique=True)
    nombres = models.CharField(max_length=80)
    primer_apellido = models.CharField(max_length=40)
    segundo_apellido = models.CharField(max_length=40)
    tipo = models.CharField(max_length=40)
    estado = models.CharField(max_length=40)

    def __str__(self):
        return self.id_persona



class informacion(models.Model):
    id_informacion = models.AutoField(primary_key=True)
    id_persona = models.ForeignKey(persona, null=True, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=128)
    estado = models.CharField(max_length=40)

    def __str__(self):
        return self.id_informacion


class solicitud(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    id_persona = models.ForeignKey(persona, null=True, on_delete=models.CASCADE)
    estado = models.CharField(max_length=40)
    monto = models.FloatField()
    tasa = models.FloatField()
    cuota = models.IntegerField()

    def __str__(self):
        return self.id_solicitud


class empleados(models.Model):
    id_persona = models.AutoField(primary_key=True)
    rol = models.CharField(max_length=40)
    sueldo = models.FloatField()
    usuario = models.CharField(max_length=80)
    password = models.CharField(max_length=40)
    estado = models.CharField(max_length=40)


class prestamo(models.Model):
    id_prestamo = models.AutoField(primary_key=True)
    id_solicitud = models.ForeignKey(persona, null=True, on_delete=models.CASCADE)
    monto = models.FloatField()
    tasa = models.FloatField()
    cuota = models.FloatField()
    estado = models.CharField(max_length=30)
    clasificacion = models.CharField(max_length=30)
    porciento_mora = models.FloatField()
    dias_gracia = models.IntegerField()

    def __str__(self):
        return self.id_solicitud


class garantia(models.Model):
    id_garantia = models.AutoField(primary_key=True)
    valor_tasacion = models.FloatField()
    estado = models.CharField(max_length=40)

    def __str__(self):
        return self.id_garantia


class terreno(models.Model):
    id_garantia = models.ForeignKey(garantia, null=True, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=80)


class automovil(models.Model):
    id_garantia = models.ForeignKey(garantia, null=True, on_delete=models.CASCADE)
    fabricante = models.CharField(max_length=40)
    modelo = models.CharField(max_length=40)
    anio = models.CharField(max_length=40)
    placa = models.CharField(max_length=40)
    chasis = models.CharField(max_length=40)


class prestamo_garantia(models.Model):
    id_prestamo = models.ForeignKey(prestamo, null=True, on_delete=models.CASCADE)
    id_garantia = models.ForeignKey(garantia, null=True, on_delete=models.CASCADE)


class cobro(models.Model):
    id_cobro = models.AutoField(primary_key=True)
    id_prestamo = models.ForeignKey(prestamo, null=True, on_delete=models.CASCADE)
    fecha = models.DateField()
    monto_total = models.FloatField()
    monto_interes = models.FloatField()
    monto_capital = models.FloatField()
    estado = models.CharField(max_length=40)


class desembolso(models.Model):
    id_desembolso = models.AutoField(primary_key=True)
    id_prestamo = models.ForeignKey(prestamo, null=True, on_delete=models.CASCADE)
    monto_total = models.FloatField(unique=True)
    codigo_cuenta_cheque = models.CharField(max_length=40)
    fecha = models.DateField()
    tipo = models.CharField(max_length=40)
    estado = models.CharField(max_length=40)


class notas(models.Model):
    id_nota = models.AutoField(primary_key=True)
    id_prestamo = models.ForeignKey(prestamo, null=True, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=40)
    monto_total = models.FloatField(unique=True)
    monto_interes = models.FloatField(unique=True)
    monto_capital = models.FloatField(unique=True)
    fecha = models.DateField()
    estado = models.CharField(max_length=40)
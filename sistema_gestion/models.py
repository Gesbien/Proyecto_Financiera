from django.db import models

# Create your models here.
class persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=15,unique=True)
    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    direccion = models.CharField(max_length=256)
    telefono = models.CharField(max_length=20)
    celular = models.CharField(max_length=20)
    tipo = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)

    def __str__(self):
        return str(self.cedula)

class informacion_trabajo(models.Model):
    id_info = models.AutoField(primary_key=True)
    cedula = models.ForeignKey(persona, null=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=70)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=256)
    sueldo = models.FloatField()

    def __str__(self):
        return str(self.id_info)

class solicitud(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    cedula = models.ForeignKey(persona, null=True, on_delete=models.CASCADE)
    estado = models.CharField(max_length=40)
    monto = models.FloatField()

    def __str__(self):
        return str(self.id_solicitud)


class empleados(models.Model):
    cedula = models.ForeignKey(persona, null=True, on_delete=models.CASCADE)
    rol = models.CharField(max_length=40)
    sueldo = models.FloatField()
    usuario = models.CharField(max_length=80)
    password = models.CharField(max_length=40)
    estado = models.CharField(max_length=40)


class prestamo(models.Model):
    id_prestamo = models.AutoField(primary_key=True)
    id_solicitud = models.ForeignKey(solicitud, null=True, on_delete=models.CASCADE)
    monto = models.FloatField()
    tasa = models.FloatField()
    cuota = models.IntegerField()
    valor_cuota = models.FloatField(null=True)
    estado = models.CharField(max_length=30)
    clasificacion = models.CharField(max_length=30)
    porciento_mora = models.FloatField()
    dias_gracia = models.IntegerField()
    fecha_expedicion = models.DateField(null=True)
    fecha_expiracion = models.DateField(null=True)
    balance_actual = models.FloatField(default=0)
    balance_capital = models.FloatField(default=0)
    balance_interes = models.FloatField(default=0)


    def __str__(self):
        return self.id_solicitud

class garante(models.Model):
    id_persona = models.ForeignKey(persona, null=True, on_delete=models.CASCADE)
    id_prestamo = models.OneToOneField(prestamo,null=True,unique=True,on_delete=models.CASCADE)

class garantia(models.Model):
    id_garantia = models.AutoField(primary_key=True)
    valor_tasacion = models.FloatField()
    nombre_propetario = models.CharField(max_length=80,null=True)
    estado = models.CharField(max_length=40)
    tipo = models.CharField(max_length=40,null=True)
    fecha_expedicion = models.DateField(null=True)

    def __str__(self):
        return self.id_garantia
class prestamo_garantia(models.Model):
    id_prestamo = models.ForeignKey(prestamo, null=True, on_delete=models.CASCADE)
    id_garantia = models.ForeignKey(garantia, null=True, on_delete=models.CASCADE)

class terreno(models.Model):
    id_garantia = models.ForeignKey(garantia, null=True, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=156)
    metraje = models.FloatField(null=True)
    certificado_titulo = models.CharField(max_length=80,null=True)
    numero_parcela = models.CharField(max_length=40,null=True)

class automovil(models.Model):
    id_garantia = models.ForeignKey(garantia, null=True, on_delete=models.CASCADE)
    fabricante = models.CharField(max_length=25)
    modelo = models.CharField(max_length=40)
    anio = models.CharField(max_length=5)
    placa = models.CharField(max_length=11)
    chasis = models.CharField(max_length=11)
    pasajeros = models.IntegerField(default=2,null=True)
    no_motor = models.CharField(max_length=15,null=True)
    color = models.CharField(max_length=10,null=True)
    clasificacion = models.CharField(max_length=15,null=True)

class cobro(models.Model):
    id_cobro = models.AutoField(primary_key=True)
    id_prestamo = models.ForeignKey(prestamo, null=True, on_delete=models.CASCADE)
    fecha = models.DateField()
    monto_total = models.FloatField()
    monto_interes = models.FloatField()
    monto_capital = models.FloatField()
    estado = models.CharField(max_length=40)
    concepto = models.CharField(max_length=150, null=True)


class desembolso(models.Model):
    id_desembolso = models.AutoField(primary_key=True)
    id_prestamo = models.ForeignKey(prestamo, null=True, on_delete=models.CASCADE)
    monto_total = models.FloatField()
    codigo_cuenta_cheque = models.CharField(max_length=40)
    fecha= models.DateField(null=True)
    tipo = models.CharField(max_length=40)
    estado = models.CharField(max_length=40)
    nombre_cliente = models.CharField(max_length=30, null=True)


class notas(models.Model):
    id_nota = models.AutoField(primary_key=True)
    id_prestamo = models.ForeignKey(prestamo, null=True, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=40)
    monto_total = models.FloatField()
    monto_interes = models.FloatField()
    monto_capital = models.FloatField()
    fecha = models.DateField()
    estado = models.CharField(max_length=40)
    concepto = models.CharField(max_length=150, null=True)

class marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre_marca = models.CharField(max_length=155)

class modelo(models.Model):
    id_modelo = models.AutoField(primary_key=True)
    nombre_marca = models.CharField(max_length=155)
    nombre_modelo = models.CharField(max_length=255)
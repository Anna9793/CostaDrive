
from django.db import models


class CategoriasVehiculo(models.Model):
    id_categoria = models.FloatField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=30)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categorias_vehiculo'
        app_label = 'CostaDriveApp'


class Clientes(models.Model):
    id_cliente = models.FloatField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(unique=True, max_length=20)
    telefono = models.CharField(max_length=20)
    email = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'clientes'
        app_label = 'CostaDriveApp'


class Facturas(models.Model):
    id_factura = models.FloatField(primary_key=True)
    id_reserva = models.OneToOneField('Reservas', models.DO_NOTHING, db_column='id_reserva')
    fecha_factura = models.DateField()
    importe_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pago = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'facturas'
        app_label = 'CostaDriveApp'


class Incidencias(models.Model):
    id_incidencia = models.FloatField(primary_key=True)
    id_reserva = models.ForeignKey('Reservas', models.DO_NOTHING, db_column='id_reserva')
    fecha_incidencia = models.DateField()
    descripcion = models.CharField(max_length=300)
    coste = models.DecimalField(max_digits=10, decimal_places=2)
    destino_coste = models.CharField(max_length=20, blank=True, null=True)
    estado_incidencia = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'incidencias'
        app_label = 'CostaDriveApp'


class Mantenimientos(models.Model):
    id_mantenimiento = models.FloatField(primary_key=True)
    id_vehiculo = models.ForeignKey('Vehiculos', models.DO_NOTHING, db_column='id_vehiculo')
    fecha_mantenimiento = models.DateField()
    descripcion = models.CharField(max_length=200)
    coste = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'mantenimientos'
        app_label = 'CostaDriveApp'


class Pagos(models.Model):
    id_pago = models.FloatField(primary_key=True)
    id_factura = models.ForeignKey(Facturas, models.DO_NOTHING, db_column='id_factura')
    fecha_pago = models.DateField()
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'pagos'
        app_label = 'CostaDriveApp'

class Reservas(models.Model):
    id_reserva = models.FloatField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='id_cliente')
    id_vehiculo = models.ForeignKey('Vehiculos', models.DO_NOTHING, db_column='id_vehiculo')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_reserva = models.DateField()
    estado_reserva = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'reservas'
        app_label = 'CostaDriveApp'


class Vehiculos(models.Model):
    id_vehiculo = models.FloatField(primary_key=True)
    id_categoria = models.ForeignKey(CategoriasVehiculo, models.DO_NOTHING, db_column='id_categoria')
    matricula = models.CharField(unique=True, max_length=20)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField()
    combustible = models.CharField(max_length=20)
    precio_dia = models.DecimalField(max_digits=8, decimal_places=2)
    estado_vehiculo = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'vehiculos'
        app_label = 'CostaDriveApp'

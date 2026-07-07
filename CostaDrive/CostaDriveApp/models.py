# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class (models.Model):
    id = models.FloatField(primary_key=True)

    class Meta:
        managed = False
        db_table = ');'


class CategoriasVehiculo(models.Model):
    id_categoria = models.FloatField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=30)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categorias_vehiculo'


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


class Clientesalumnos(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido1 = models.CharField(max_length=50, blank=True, null=True)
    apellido2 = models.CharField(max_length=50, blank=True, null=True)
    domicilio = models.CharField(max_length=50, blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    sexo = models.CharField(max_length=50, blank=True, null=True)
    sistema = models.CharField(max_length=50, blank=True, null=True)
    comentarios = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clientesalumnos'


class Dept(models.Model):
    dept_no = models.IntegerField(primary_key=True)
    dnombre = models.CharField(max_length=30, blank=True, null=True)
    loc = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dept'


class Distribuidoras(models.Model):
    iddistribuidor = models.IntegerField(primary_key=True)
    distribuidor = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    paginaweb = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.IntegerField(blank=True, null=True)
    contacto = models.CharField(max_length=50, blank=True, null=True)
    logo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'distribuidoras'


class Doctor(models.Model):
    hospital_cod = models.ForeignKey('Hospital', models.DO_NOTHING, db_column='hospital_cod', blank=True, null=True)
    doctor_no = models.IntegerField(primary_key=True)
    apellido = models.CharField(max_length=20)
    especialidad = models.CharField(max_length=13, blank=True, null=True)
    salario = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctor'


class Emp(models.Model):
    emp_no = models.IntegerField(primary_key=True)
    apellido = models.CharField(max_length=10, blank=True, null=True)
    oficio = models.CharField(max_length=10, blank=True, null=True)
    dir = models.IntegerField(blank=True, null=True)
    fecha_alt = models.DateField(blank=True, null=True)
    salario = models.IntegerField(blank=True, null=True)
    comision = models.IntegerField(blank=True, null=True)
    dept_no = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emp'


class Enfermo(models.Model):
    inscripcion = models.IntegerField(primary_key=True)
    apellido = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=20, blank=True, null=True)
    fecha_nac = models.DateField(blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    nss = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enfermo'


class Facturas(models.Model):
    id_factura = models.FloatField(primary_key=True)
    id_reserva = models.OneToOneField('Reservas', models.DO_NOTHING, db_column='id_reserva')
    fecha_factura = models.DateField()
    importe_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pago = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'facturas'


class Generos(models.Model):
    idgenero = models.IntegerField(primary_key=True)
    genero = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'generos'


class Hospital(models.Model):
    hospital_cod = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=19)
    direccion = models.CharField(max_length=20, blank=True, null=True)
    telefono = models.CharField(max_length=9, blank=True, null=True)
    num_cama = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hospital'


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


class Mantenimientos(models.Model):
    id_mantenimiento = models.FloatField(primary_key=True)
    id_vehiculo = models.ForeignKey('Vehiculos', models.DO_NOTHING, db_column='id_vehiculo')
    fecha_mantenimiento = models.DateField()
    descripcion = models.CharField(max_length=200)
    coste = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'mantenimientos'


class Nacionalidad(models.Model):
    idnacionalidad = models.IntegerField(primary_key=True)
    nacionalidad = models.CharField(max_length=50, blank=True, null=True)
    bandera = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nacionalidad'


class Ocupacion(models.Model):
    inscripcion = models.ForeignKey(Enfermo, models.DO_NOTHING, db_column='inscripcion')
    hospital_cod = models.ForeignKey('Sala', models.DO_NOTHING, db_column='hospital_cod')
    sala_cod = models.ForeignKey('Sala', models.DO_NOTHING, db_column='sala_cod', to_field='sala_cod', related_name='ocupacion_sala_cod_set')
    cama = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ocupacion'


class Pagos(models.Model):
    id_pago = models.FloatField(primary_key=True)
    id_factura = models.ForeignKey(Facturas, models.DO_NOTHING, db_column='id_factura')
    fecha_pago = models.DateField()
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'pagos'


class Pedidos(models.Model):
    idcliente = models.IntegerField(primary_key=True)  # The composite primary key (idcliente, idpelicula) found, that is not supported. The first column is selected.
    idpelicula = models.IntegerField()
    cantidad = models.IntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    precio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pedidos'
        unique_together = (('idcliente', 'idpelicula'),)


class Peliculas(models.Model):
    idpelicula = models.IntegerField(primary_key=True)
    iddistribuidor = models.IntegerField(blank=True, null=True)
    idgenero = models.IntegerField(blank=True, null=True)
    titulo = models.CharField(max_length=255, blank=True, null=True)
    idnacionalidad = models.IntegerField(blank=True, null=True)
    argumento = models.CharField(max_length=1550, blank=True, null=True)
    foto = models.CharField(max_length=50, blank=True, null=True)
    fecha_estreno = models.DateField(blank=True, null=True)
    actores = models.CharField(max_length=1550, blank=True, null=True)
    director = models.CharField(max_length=50, blank=True, null=True)
    duracion = models.IntegerField(blank=True, null=True)
    precio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'peliculas'


class Plantilla(models.Model):
    hospital_cod = models.ForeignKey('Sala', models.DO_NOTHING, db_column='hospital_cod')
    sala_cod = models.ForeignKey('Sala', models.DO_NOTHING, db_column='sala_cod', to_field='sala_cod', related_name='plantilla_sala_cod_set')
    empleado_no = models.IntegerField(primary_key=True)
    apellido = models.CharField(max_length=15)
    funcion = models.CharField(max_length=10, blank=True, null=True)
    turno = models.CharField(max_length=1, blank=True, null=True)
    salario = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plantilla'


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


class Sala(models.Model):
    hospital_cod = models.OneToOneField(Hospital, models.DO_NOTHING, db_column='hospital_cod', primary_key=True)  # The composite primary key (hospital_cod, sala_cod) found, that is not supported. The first column is selected.
    sala_cod = models.IntegerField()
    nombre = models.CharField(max_length=20)
    num_cama = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sala'
        unique_together = (('hospital_cod', 'sala_cod'),)


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

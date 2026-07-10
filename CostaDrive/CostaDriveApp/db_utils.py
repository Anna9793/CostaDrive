from django.db import connection
from django.utils import timezone
from datetime import timedelta
from django.db.models import F, Value, Count
from django.db.models.functions import Concat, TruncMonth
from .models import (
    CategoriasVehiculo, Clientes, Facturas, Incidencias,
    Mantenimientos, Pagos, Reservas, Vehiculos
)

def _ejecutar_proc(nombre_proc, params):
    """Ejecuta un procedimiento almacenado en Oracle."""
    with connection.cursor() as cursor:
        cursor.callproc(nombre_proc, params)

def _ejecutar_sql(sql, params=None):
    """Ejecuta una consulta SQL genérica y retorna los resultados si es un SELECT."""
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        if sql.strip().upper().startswith("SELECT"):
            return cursor.fetchall()

def obtener_reservas_db(id_cliente=None):
    """Obtiene las reservas, opcionalmente filtradas por cliente."""
    queryset = Reservas.objects.select_related('id_cliente', 'id_vehiculo', 'facturas')
    if id_cliente:
        queryset = queryset.filter(id_cliente=id_cliente)
    
    queryset = queryset.annotate(
        nombre_cliente=Concat(F('id_cliente__nombre'), Value(' '), F('id_cliente__apellidos')),
        nombre_vehiculo=Concat(F('id_vehiculo__marca'), Value(' '), F('id_vehiculo__modelo'))
    ).order_by('-fecha_reserva')
    
    raw_list = list(queryset.values_list(
        'id_reserva',
        'id_cliente',
        'id_vehiculo',
        'fecha_inicio',
        'fecha_fin',
        'fecha_reserva',
        'estado_reserva',
        'nombre_cliente',
        'nombre_vehiculo',
        'facturas__id_factura',
        'facturas__estado_pago',
        'facturas__importe_total',
        'id_vehiculo__precio_dia'
    ))
    
    result = []
    for r in raw_list:
        # Calcular importe estimado en Python para evitar problemas de conversión de tipos de fecha en el ORM de Oracle
        days = (r[4] - r[3]).days if r[4] and r[3] else 0
        estimado = r[12] * (days if days > 0 else 1) if r[12] else 0
        result.append(r[:12] + (estimado,))
    return result

def obtener_reserva_por_id_db(id_reserva):
    """Obtiene una reserva específica por su ID."""
    try:
        r = Reservas.objects.select_related('id_cliente', 'id_vehiculo').annotate(
            nombre_cliente=Concat(F('id_cliente__nombre'), Value(' '), F('id_cliente__apellidos')),
            nombre_vehiculo=Concat(F('id_vehiculo__marca'), Value(' '), F('id_vehiculo__modelo'))
        ).values_list(
            'id_reserva',
            'id_cliente',
            'id_vehiculo',
            'fecha_inicio',
            'fecha_fin',
            'fecha_reserva',
            'estado_reserva',
            'nombre_cliente',
            'nombre_vehiculo'
        ).get(id_reserva=id_reserva)
        return r
    except Reservas.DoesNotExist:
        return None

def actualizar_fechas_reserva_db(id_reserva, nuevo_inicio, nuevo_fin):
    """Llama al procedimiento almacenado SP_ACTUALIZAR_RESERVA para modificar las fechas."""
    _ejecutar_proc('SP_ACTUALIZAR_RESERVA', [id_reserva, nuevo_inicio, nuevo_fin])

def contar_reservas_pendientes_db():
    """Cuenta el número de facturas con estado de pago PENDIENTE."""
    return Facturas.objects.filter(estado_pago='PENDIENTE').count()

def crear_reserva_db(id_cliente, id_vehiculo, fecha_inicio, fecha_fin):
    """Llama al procedimiento almacenado CREAR_RESERVA."""
    _ejecutar_proc('CREAR_RESERVA', [id_cliente, id_vehiculo, fecha_inicio, fecha_fin])

def cancelar_reserva_db(id_reserva):
    """Llama al procedimiento almacenado CANCELAR_RESERVA."""
    _ejecutar_proc('CANCELAR_RESERVA', [id_reserva])

def generar_factura_db(id_reserva):
    """Llama al procedimiento almacenado GENERAR_FACTURA."""
    _ejecutar_proc('GENERAR_FACTURA', [id_reserva])
    
def registrar_pago_db(id_factura, metodo_pago, importe):
    """Llama al procedimiento almacenado REGISTRAR_PAGO."""
    _ejecutar_proc('REGISTRAR_PAGO', [id_factura, metodo_pago, importe])

def obtener_vehiculos_db():
    """Obtiene todos los vehículos con su información de categoría."""
    return list(Vehiculos.objects.select_related('id_categoria').order_by('-id_vehiculo').values_list(
        'id_vehiculo',
        'matricula',
        'marca',
        'modelo',
        'anio',
        'combustible',
        'precio_dia',
        'estado_vehiculo',
        'id_categoria__nombre'
    ))

def registrar_mantenimiento_db(id_vehiculo, descripcion, coste):
    """Calls the atomic PL/SQL procedure."""
    # Just one call, the database handles the integrity!
    _ejecutar_proc('REGISTRAR_MANTENIMIENTO', [id_vehiculo, descripcion, coste])

def liberar_vehiculo_mantenimiento_db(id_vehiculo):
    """Devuelve un vehículo del mantenimiento a DISPONIBLE."""
    Vehiculos.objects.filter(id_vehiculo=id_vehiculo).update(estado_vehiculo='DISPONIBLE')

def obtener_facturas_db():
    """Obtiene todas las facturas con la información de cliente y reserva."""
    queryset = Facturas.objects.select_related('id_reserva__id_cliente', 'id_reserva__id_vehiculo').annotate(
        cliente=Concat(F('id_reserva__id_cliente__nombre'), Value(' '), F('id_reserva__id_cliente__apellidos')),
        vehiculo=Concat(F('id_reserva__id_vehiculo__marca'), Value(' '), F('id_reserva__id_vehiculo__modelo'))
    ).order_by('-fecha_factura')
    return list(queryset.values_list(
        'id_factura',
        'id_reserva',
        'fecha_factura',
        'importe_total',
        'estado_pago',
        'cliente',
        'vehiculo'
    ))

def obtener_factura_por_id_db(id_factura):
    """Obtiene una factura específica por su ID."""
    try:
        queryset = Facturas.objects.select_related('id_reserva__id_cliente', 'id_reserva__id_vehiculo').annotate(
            cliente=Concat(F('id_reserva__id_cliente__nombre'), Value(' '), F('id_reserva__id_cliente__apellidos')),
            vehiculo=Concat(F('id_reserva__id_vehiculo__marca'), Value(' '), F('id_reserva__id_vehiculo__modelo'))
        )
        return queryset.values_list(
            'id_factura',
            'id_reserva',
            'fecha_factura',
            'importe_total',
            'estado_pago',
            'cliente',
            'vehiculo'
        ).get(id_factura=id_factura)
    except Facturas.DoesNotExist:
        return None

def obtener_incidencias_db():
    """Obtiene todas las incidencias de los alquileres."""
    queryset = Incidencias.objects.select_related('id_reserva__id_cliente', 'id_reserva__id_vehiculo').annotate(
        cliente=Concat(F('id_reserva__id_cliente__nombre'), Value(' '), F('id_reserva__id_cliente__apellidos')),
        vehiculo=Concat(F('id_reserva__id_vehiculo__marca'), Value(' '), F('id_reserva__id_vehiculo__modelo'))
    ).order_by('-fecha_incidencia')
    return list(queryset.values_list(
        'id_incidencia',
        'id_reserva',
        'fecha_incidencia',
        'descripcion',
        'coste',
        'destino_coste',
        'estado_incidencia',
        'cliente',
        'vehiculo'
    ))

def obtener_mantenimientos_db():
    """Obtiene el historial de mantenimientos de los vehículos."""
    queryset = Mantenimientos.objects.select_related('id_vehiculo').annotate(
        vehiculo=Concat(F('id_vehiculo__marca'), Value(' '), F('id_vehiculo__modelo'))
    ).order_by('-fecha_mantenimiento')
    return list(queryset.values_list(
        'id_mantenimiento',
        'id_vehiculo',
        'fecha_mantenimiento',
        'descripcion',
        'coste',
        'vehiculo',
        'id_vehiculo__matricula'
    ))

def crear_incidencia_db(id_reserva, descripcion, coste, destino_coste):
    """Inserta una nueva incidencia en estado ABIERTA."""
    Incidencias.objects.create(
        id_reserva=Reservas.objects.get(id_reserva=id_reserva),
        fecha_incidencia=timezone.now().date(),
        descripcion=descripcion,
        coste=coste,
        destino_coste=destino_coste,
        estado_incidencia='ABIERTA'
    )

def resolver_incidencia_db(id_incidencia, coste_final):
    """Llama al procedimiento almacenado RESOLVER_INCIDENCIA."""
    _ejecutar_proc('RESOLVER_INCIDENCIA', [id_incidencia, coste_final])

def crear_cliente_db(nombre, apellidos, dni, telefono, email):
    """Inserta un nuevo cliente en la base de datos y devuelve su ID generado."""
    Clientes.objects.create(
        nombre=nombre,
        apellidos=apellidos,
        dni=dni,
        telefono=telefono,
        email=email
    )
    try:
        return Clientes.objects.get(dni=dni).id_cliente
    except Clientes.DoesNotExist:
        return None

def obtener_clientes_db():
    """Obtiene todos los clientes con su número de reservas asociadas."""
    queryset = Clientes.objects.annotate(
        num_reservas=Count('reservas')
    ).order_by('nombre', 'apellidos')
    return list(queryset.values_list(
        'id_cliente',
        'nombre',
        'apellidos',
        'dni',
        'telefono',
        'email',
        'num_reservas'
    ))

def obtener_tendencia_mensual_db():
    """Obtiene el número de reservas por mes en los últimos 6 meses."""
    cutoff = timezone.now().date() - timedelta(days=180)
    queryset = Reservas.objects.filter(fecha_reserva__gte=cutoff).annotate(
        mes=TruncMonth('fecha_reserva')
    ).values('mes').annotate(total=Count('id_reserva')).order_by('mes')
    return [(r['mes'].strftime('%Y-%m') if r['mes'] else '', r['total']) for r in queryset]

def obtener_distribucion_categorias_db():
    """Obtiene el desglose de reservas por categoría de vehículo."""
    queryset = Reservas.objects.values(
        'id_vehiculo__id_categoria__nombre'
    ).annotate(
        total=Count('id_reserva')
    ).order_by('-total')
    return [(r['id_vehiculo__id_categoria__nombre'], r['total']) for r in queryset]

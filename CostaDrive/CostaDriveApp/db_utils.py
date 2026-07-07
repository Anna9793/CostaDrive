from django.db import connection

def _ejecutar_proc(nombre_proc, params):

    with connection.cursor() as cursor:
        cursor.callproc(nombre_proc, params)

def crear_reserva_db(id_cliente, id_vehiculo, fecha_inicio, fecha_fin):

    params = [id_cliente, id_vehiculo, fecha_inicio, fecha_fin]
    
    _ejecutar_proc('CREAR_RESERVA', params)

def generar_factura_db(id_reserva):

    params = [id_reserva]

    _ejecutar_proc('GENERAR_FACTURA', params)
    
def registrar_pago_db(id_factura, metodo_pago, importe):

    params = [id_factura, metodo_pago, importe]

    _ejecutar_proc('REGISTRAR_PAGO', params)

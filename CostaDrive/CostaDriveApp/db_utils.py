from django.db import connection
import oracledb

def _ejecutar_proc(nombre_proc, params):

    with connection.cursor() as cursor:
        cursor.callproc(nombre_proc, params)

def _ejecutar_sql(sql, params=None):
    with connection as cursor:
        cursor.execute(sql, params)
        if sql.strip().upper().startswith("SELECT"):
            return cursor.fetchall()

def obtener_reservas_db(id_cliente=None):
    if id_cliente:
        query = "SELECT * FROM RESERVAS WHERE id_cliente = :1 ORDER BY fecha_inicio DESC"
        return _ejecutar_sql(query, [id_cliente])
    else:
        return _ejecutar_sql("SELECT * FROM RESERVAS ORDER BY fecha_incio DESC")

def actualizar_fechas_reserva_db(id_reserva, nuevo_inicio, nuevo_fin):
    sql = """
        UPDATE RESERVAS
        SET fecha_inicio = :1, fecha_fin = :2
        WHERE id_reserva = :3
    """
    _ejecutar_sql(sql, [nuevo_inicio, nuevo_fin, id_reserva])

def contar_reservas_pendientes_db():
    query = "SELECT COUNT(*) FROM RESERVAS WHERE estado_reserva='PENDIENTE'"
    resultado = _ejecutar_sql(query)
    return resultado[0][0]

def crear_reserva_db(id_cliente, id_vehiculo, fecha_incio, fecha_fin):
    params = [id_cliente, id_vehiculo, fecha_incio, fecha_fin]
    _ejecutar_proc('CREAR_RESERVA', params)

def cancelar_reserva_db(id_reserva):
    params = [id_reserva]
    _ejecutar_proc('CANCELAR_RESERVA', params)

def generar_factura_db(id_reserva):

    params = [id_reserva]

    _ejecutar_proc('GENERAR_FACTURA', params)
    
def registrar_pago_db(id_factura, metodo_pago, importe):

    params = [id_factura, metodo_pago, importe]

    _ejecutar_proc('REGISTRAR_PAGO', params)


from django.db import connection

def crear_reserva_db(id_cliente, id_vehiculo, fecha_inicio, fecha_fin):

    lista_parametros = [id_cliente, id_vehiculo, fecha_inicio, fecha_fin]
    
    with connection.cursor() as cursor:
        cursor.callproc('CREAR_RESERVA', lista_parametros)

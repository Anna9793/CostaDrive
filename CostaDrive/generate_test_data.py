import os
import django
from datetime import date, timedelta, datetime
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CostaDrive.settings')
django.setup()

from django.db import connection

def _ejecutar_sql(sql, params=None):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        if sql.strip().upper().startswith("SELECT"):
            return cursor.fetchall()

def limpiar_tablas():
    print("Limpiando datos existentes de las tablas para evitar conflictos...")
    # Desactivar temporalmente restricciones de FK para una limpieza limpia y rápida
    try:
        _ejecutar_sql("ALTER TABLE PAGOS DISABLE CONSTRAINT FK_PAGO_FACTURA")
    except Exception: pass
    try:
        _ejecutar_sql("ALTER TABLE FACTURAS DISABLE CONSTRAINT FK_FACTURA_RESERVA")
    except Exception: pass
    try:
        _ejecutar_sql("ALTER TABLE INCIDENCIAS DISABLE CONSTRAINT FK_INCIDENCIA_RESERVA")
    except Exception: pass
    try:
        _ejecutar_sql("ALTER TABLE MANTENIMIENTOS DISABLE CONSTRAINT FK_MANTENIMIENTO_VEHICULO")
    except Exception: pass
    try:
        _ejecutar_sql("ALTER TABLE RESERVAS DISABLE CONSTRAINT FK_RESERVA_CLIENTE")
    except Exception: pass
    try:
        _ejecutar_sql("ALTER TABLE RESERVAS DISABLE CONSTRAINT FK_RESERVA_VEHICULO")
    except Exception: pass
    try:
        _ejecutar_sql("ALTER TABLE VEHICULOS DISABLE CONSTRAINT FK_VEHICULO_CATEGORIA")
    except Exception: pass

    # Borrar registros
    _ejecutar_sql("DELETE FROM PAGOS")
    _ejecutar_sql("DELETE FROM FACTURAS")
    _ejecutar_sql("DELETE FROM INCIDENCIAS")
    _ejecutar_sql("DELETE FROM MANTENIMIENTOS")
    _ejecutar_sql("DELETE FROM RESERVAS")
    _ejecutar_sql("DELETE FROM VEHICULOS")
    _ejecutar_sql("DELETE FROM CLIENTES")
    _ejecutar_sql("DELETE FROM CATEGORIAS_VEHICULO")

    # Rehabilitar restricciones
    try:
        _ejecutar_sql("ALTER TABLE PAGOS ENABLE CONSTRAINT FK_PAGO_FACTURA")
    except Exception: pass
    try:
        _ejecutar_sql("ALTER TABLE FACTURAS ENABLE CONSTRAINT FK_FACTURA_RESERVA")
    except Exception: pass
    try:
        _ejecutar_sql("ALTER TABLE INCIDENCIAS ENABLE CONSTRAINT FK_INCIDENCIA_RESERVA")
    except Exception: pass
    try:
        _ejecutar_sql("ALTER TABLE MANTENIMIENTOS ENABLE CONSTRAINT FK_MANTENIMIENTO_VEHICULO")
    except Exception: pass
    try:
        _ejecutar_sql("ALTER TABLE RESERVAS ENABLE CONSTRAINT FK_RESERVA_CLIENTE")
    except Exception: pass
    try:
        _ejecutar_sql("ALTER TABLE RESERVAS ENABLE CONSTRAINT FK_RESERVA_VEHICULO")
    except Exception: pass
    try:
        _ejecutar_sql("ALTER TABLE VEHICULOS ENABLE CONSTRAINT FK_VEHICULO_CATEGORIA")
    except Exception: pass
    print("Tablas limpiadas con éxito.")

def generar_datos():
    # 1. Crear Categorías
    print("Creando categorías...")
    categorias_data = [
        (1, 'ECONOMICO', 'Vehículos pequeños, utilitarios y de bajo consumo.'),
        (2, 'COMPACTO', 'Coches urbanos de tamaño medio ideales para el día a día.'),
        (3, 'SUV', 'Coches amplios, con posición de conducción elevada y adaptables.'),
        (4, 'FAMILIAR', 'Monovolúmenes y rancheras con gran espacio de maletero.'),
        (5, 'PREMIUM', 'Vehículos de gama alta, berlinas de lujo y altas prestaciones.')
    ]
    
    for cid, nombre, desc in categorias_data:
        _ejecutar_sql("""
            INSERT INTO CATEGORIAS_VEHICULO (id_categoria, nombre, descripcion)
            VALUES (%s, %s, %s)
        """, [cid, nombre, desc])

    # 2. Crear Clientes (retornar IDs)
    print("Creando clientes...")
    clientes_data = [
        ('Juan', 'Pérez García', '12345678X', '600111222', 'juan.perez@example.com'),
        ('María', 'López Fernández', '87654321Y', '611222333', 'maria.lopez@example.com'),
        ('Carlos', 'Martín Soler', '23456789Z', '622333444', 'carlos.martin@example.com'),
        ('Laura', 'Gómez Ruiz', '34567890A', '633444555', 'laura.gomez@example.com'),
        ('David', 'Sánchez Ortiz', '45678901B', '644555666', 'david.sanchez@example.com'),
        ('Elena', 'Navarro Gil', '56789012C', '655666777', 'elena.navarro@example.com'),
        ('Pedro', 'Vázquez Albiol', '67890123D', '666777888', 'pedro.vazquez@example.com'),
        ('Sofía', 'Castro Durán', '78901234E', '677888999', 'sofia.castro@example.com'),
        ('Javier', 'Ramos Moreno', '89012345F', '688999000', 'javier.ramos@example.com'),
        ('Lucía', 'Herrero Sanz', '90123456G', '699000111', 'lucia.herrero@example.com')
    ]
    
    cliente_ids = []
    for nom, ape, dni, tel, mail in clientes_data:
        _ejecutar_sql("""
            INSERT INTO CLIENTES (nombre, apellidos, dni, telefono, email)
            VALUES (%s, %s, %s, %s, %s)
        """, [nom, ape, dni, tel, mail])
        res = _ejecutar_sql("SELECT id_cliente FROM CLIENTES WHERE dni = %s", [dni])
        cliente_ids.append(res[0][0])

    # 3. Crear Vehículos
    print("Creando vehículos...")
    vehiculos_data = [
        (1, '1234-KBB', 'Renault', 'Clio', 2022, 'GASOLINA', 25.00, 'DISPONIBLE'),
        (1, '5678-LCC', 'Fiat', '500 Hybrid', 2023, 'HIBRIDO', 28.00, 'DISPONIBLE'),
        (1, '9012-MDD', 'Toyota', 'Yaris', 2024, 'HIBRIDO', 32.00, 'DISPONIBLE'),
        
        (2, '3456-KFF', 'Seat', 'León', 2023, 'GASOLINA', 40.00, 'DISPONIBLE'),
        (2, '7890-LGG', 'Volkswagen', 'Golf', 2024, 'HIBRIDO', 45.00, 'DISPONIBLE'),
        (2, '2345-MHH', 'Toyota', 'Corolla', 2024, 'HIBRIDO', 42.00, 'ALQUILADO'),
        
        (3, '6789-KLL', 'Hyundai', 'Tucson', 2023, 'HIBRIDO', 60.00, 'DISPONIBLE'),
        (3, '0123-LMM', 'Kia', 'Sportage', 2024, 'HIBRIDO', 58.00, 'ALQUILADO'),
        (3, '4567-MNN', 'Nissan', 'Qashqai', 2025, 'GASOLINA', 65.00, 'DISPONIBLE'),
        
        (4, '8901-KPP', 'Peugeot', '5008', 2023, 'DIESEL', 55.00, 'DISPONIBLE'),
        (4, '2345-LQQ', 'Skoda', 'Octavia Combi', 2024, 'DIESEL', 52.00, 'DISPONIBLE'),
        (4, '6789-MRR', 'Toyota', 'RAV4 Familiar', 2024, 'HIBRIDO', 70.00, 'MANTENIMIENTO'),
        
        (5, '0123-KSS', 'Mercedes-Benz', 'Clase C', 2024, 'DIESEL', 110.00, 'DISPONIBLE'),
        (5, '4567-LTT', 'BMW', 'Serie 3', 2025, 'HIBRIDO', 120.00, 'DISPONIBLE'),
        (5, '8901-MUU', 'Audi', 'A4 Sedan', 2025, 'DIESEL', 115.00, 'MANTENIMIENTO')
    ]
    
    vehiculo_ids = []
    vehiculo_precios = {}
    for cat_id, matr, marc, mod, anio, comb, prec, est in vehiculos_data:
        _ejecutar_sql("""
            INSERT INTO VEHICULOS (id_categoria, matricula, marca, modelo, anio, combustible, precio_dia, estado_vehiculo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, [cat_id, matr, marc, mod, anio, comb, prec, est])
        res = _ejecutar_sql("SELECT id_vehiculo FROM VEHICULOS WHERE matricula = %s", [matr])
        vid = res[0][0]
        vehiculo_ids.append(vid)
        vehiculo_precios[vid] = prec

    # 4. Crear Reservas (Mezcla de Finalizadas, Activas e Incipientes)
    print("Creando reservas...")
    hoy = date.today()
    
    # Reservas: (cliente_id, vehiculo_id, fecha_inicio, fecha_fin, estado_reserva)
    res_finalizadas = [
        (cliente_ids[0], vehiculo_ids[0], hoy - timedelta(days=20), hoy - timedelta(days=15), 'FINALIZADA'),
        (cliente_ids[1], vehiculo_ids[3], hoy - timedelta(days=18), hoy - timedelta(days=12), 'FINALIZADA'),
        (cliente_ids[2], vehiculo_ids[6], hoy - timedelta(days=15), hoy - timedelta(days=8), 'FINALIZADA'),
        (cliente_ids[3], vehiculo_ids[9], hoy - timedelta(days=10), hoy - timedelta(days=5), 'FINALIZADA'),
    ]
    
    res_activas = [
        (cliente_ids[4], vehiculo_ids[5], hoy - timedelta(days=3), hoy + timedelta(days=4), 'ACTIVA'),
        (cliente_ids[5], vehiculo_ids[7], hoy - timedelta(days=1), hoy + timedelta(days=6), 'ACTIVA'),
    ]
    
    res_futuras = [
        (cliente_ids[6], vehiculo_ids[1], hoy + timedelta(days=5), hoy + timedelta(days=12), 'ACTIVA'),
        (cliente_ids[7], vehiculo_ids[4], hoy + timedelta(days=10), hoy + timedelta(days=15), 'ACTIVA'),
    ]
    
    todas_reservas = res_finalizadas + res_activas + res_futuras
    reserva_ids = []
    reserva_vehiculos = {}
    reserva_dias = {}
    
    for cid, vid, ini, fin, est in todas_reservas:
        fecha_res = ini - timedelta(days=random.randint(2, 10))
        # Formatear fechas como strings de Oracle
        ini_str = ini.strftime('%Y-%m-%d')
        fin_str = fin.strftime('%Y-%m-%d')
        fecha_res_str = fecha_res.strftime('%Y-%m-%d')
        
        _ejecutar_sql("""
            INSERT INTO RESERVAS (id_cliente, id_vehiculo, fecha_inicio, fecha_fin, fecha_reserva, estado_reserva)
            VALUES (%s, %s, TO_DATE(%s, 'YYYY-MM-DD'), TO_DATE(%s, 'YYYY-MM-DD'), TO_DATE(%s, 'YYYY-MM-DD'), %s)
        """, [cid, vid, ini_str, fin_str, fecha_res_str, est])
        
        res = _ejecutar_sql("""
            SELECT id_reserva FROM RESERVAS 
            WHERE id_cliente = %s AND id_vehiculo = %s AND fecha_inicio = TO_DATE(%s, 'YYYY-MM-DD')
        """, [cid, vid, ini_str])
        
        rid = res[0][0]
        reserva_ids.append(rid)
        reserva_vehiculos[rid] = vid
        dias = (fin - ini).days
        reserva_dias[rid] = dias if dias > 0 else 1

    # 5. Generar Facturas y Pagos correspondientes
    print("Generando facturas y cobros asociados...")
    for index, rid in enumerate(reserva_ids):
        vid = reserva_vehiculos[rid]
        precio = vehiculo_precios[vid]
        dias = reserva_dias[rid]
        importe = precio * dias
        
        # Para reservas finalizadas o las activas pasadas, generamos factura
        if index < 6: # Primeras 6 reservas (finalizadas + activas actuales)
            # 3 facturas pagadas, 2 pendientes, 1 anulada
            if index in [0, 1, 4]:
                estado_pago = 'PAGADA'
            elif index in [2, 5]:
                estado_pago = 'PENDIENTE'
            else:
                estado_pago = 'ANULADA'
                
            _ejecutar_sql("""
                INSERT INTO FACTURAS (id_reserva, fecha_factura, importe_total, estado_pago)
                VALUES (%s, SYSDATE - 4, %s, %s)
            """, [rid, importe, estado_pago])
            
            res = _ejecutar_sql("SELECT id_factura FROM FACTURAS WHERE id_reserva = %s", [rid])
            fid = res[0][0]
            
            # Registrar Pago si está PAGADA
            if estado_pago == 'PAGADA':
                _ejecutar_sql("""
                    INSERT INTO PAGOS (id_factura, fecha_pago, importe, metodo_pago)
                    VALUES (%s, SYSDATE - 3, %s, %s)
                """, [fid, importe, random.choice(['TARJETA', 'EFECTIVO', 'TRANSFERENCIA'])])

    # 6. Crear Incidencias (Una abierta, otra resuelta)
    print("Creando incidencias de prueba...")
    # Incidencia abierta en la reserva de David (index 4 / reserva_ids[4])
    _ejecutar_sql("""
        INSERT INTO INCIDENCIAS (id_reserva, fecha_incidencia, descripcion, coste, destino_coste, estado_incidencia)
        VALUES (%s, SYSDATE - 2, %s, 120.00, 'CLIENTE', 'ABIERTA')
    """, [reserva_ids[4], "Arañazo profundo en aleta trasera derecha al aparcar en garaje público."])
    
    # Incidencia resuelta en la reserva finalizada de María (index 1 / reserva_ids[1])
    _ejecutar_sql("""
        INSERT INTO INCIDENCIAS (id_reserva, fecha_incidencia, descripcion, coste, destino_coste, estado_incidencia)
        VALUES (%s, SYSDATE - 10, %s, 85.00, 'EMPRESA', 'RESUELTA')
    """, [reserva_ids[1], "Fallo en válvula de aire acondicionado. Aire no enfría de forma regular."])
    
    # 7. Crear Mantenimientos (uno por la incidencia y otro general)
    print("Creando registros de mantenimiento...")
    # Registro por la incidencia resuelta de la empresa (se mete en taller de Toyota RAV4)
    _ejecutar_sql("""
        INSERT INTO MANTENIMIENTOS (id_vehiculo, fecha_mantenimiento, descripcion, coste)
        VALUES (%s, SYSDATE - 5, %s, 240.00)
    """, [vehiculo_ids[11], "Revisión rutinaria de los 60.000km, cambio de bujías y líquido refrigerante."])
    
    # Mantenimiento del Audi A4 por el AC roto
    _ejecutar_sql("""
        INSERT INTO MANTENIMIENTOS (id_vehiculo, fecha_mantenimiento, descripcion, coste)
        VALUES (%s, SYSDATE - 9, %s, 85.00)
    """, [vehiculo_ids[14], "Reparación del sistema de climatización tras reporte de fallo (Válvula AC)."])

    print("¡Base de datos cargada con éxito con datos coherentes!")

if __name__ == '__main__':
    limpiar_tablas()
    generar_datos()

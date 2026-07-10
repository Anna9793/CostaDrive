import os
import django
from datetime import date, timedelta
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
    print("Limpiando datos existentes de las tablas...")
    # Desactivar temporalmente restricciones de FK
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

def cargar_datos_originales_dinamico():
    print("Cargando datos originales dinámicamente para resolver IDs autogenerados...")
    
    # 1. Categorías
    categorias = [
        (1, 'ECONOMICO', 'Vehículos pequeños y de bajo consumo'),
        (2, 'COMPACTO', 'Vehículos urbanos de tamaño medio'),
        (3, 'SUV', 'Vehículos deportivos utilitarios'),
        (4, 'FAMILIAR', 'Vehículos amplios para familias'),
        (5, 'PREMIUM', 'Vehículos de gama alta')
    ]
    for cid, nombre, desc in categorias:
        _ejecutar_sql("INSERT INTO CATEGORIAS_VEHICULO (id_categoria, nombre, descripcion) VALUES (%s, %s, %s)", [cid, nombre, desc])

    # 2. Clientes
    clientes = [
        ('Carlos', 'Sanchez Gómez','23456789B','600222222','carlos@email.com'),
        ('Ana','Martinez González', '12345678A','600111111', 'ana@email.com'),
        ('Alejandro', 'Sánchez Ruiz', '12345678Q', '654123987', 'asanchez@email.com'),
        ('Beatriz', 'Gómez Martín', '87654321W', '698741236', 'bgomez@email.com'),
        ('Javier', 'López Pérez', '11223344E', '612345678', 'jlopez@email.com'),
        ('Lucía', 'Fernández Gil', '99887766R', '678990112', 'lfernandez@email.com'),
        ('Miguel', 'Díaz Castro', '55443322T', '633445566', 'mdiaz@email.com' ),
        ('Elena', 'Ruiz Moreno', '66778899Y', '644556677', 'eruiz@email.com'),
        ('Carlos', 'Jiménez Ruiz', '44332211U', '655667788', 'cjimenez@email.com'),
        ('Sofía', 'Álvarez Navarro', '33221100I', '666778899', 'salvarez@email.com'),
        ('Pablo', 'Moreno Ortiz', '22110099O', '677889900', 'pmoreno@email.com'),
        ('Isabel', 'Vázquez Herrera', '11009988P', '688990011', 'ivazquez@email.com')
    ]
    client_map = {}
    for nom, ape, dni, tel, mail in clientes:
        _ejecutar_sql("INSERT INTO CLIENTES (nombre, apellidos, dni, telefono, email) VALUES (%s, %s, %s, %s, %s)", [nom, ape, dni, tel, mail])
        res = _ejecutar_sql("SELECT id_cliente FROM CLIENTES WHERE dni = %s", [dni])
        client_map[dni] = res[0][0]

    # 3. Vehículos
    vehiculos = [
        (1, '1111-AAA', 'Seat', 'Ibiza', 2023, 'GASOLINA', 30.00, 'DISPONIBLE'),
        (1, '2222-BBB', 'Fiat', '500', 2024, 'GASOLINA', 28.00, 'DISPONIBLE'),
        (1, '3333-CCC', 'Kia', 'Picanto', 2022, 'GASOLINA', 25.00, 'DISPONIBLE'),
        (2, '4444-DDD', 'Volkswagen', 'Golf', 2023, 'HIBRIDO', 45.00, 'DISPONIBLE'),
        (2, '5555-EEE', 'Toyota', 'Corolla', 2024, 'HIBRIDO', 48.00, 'DISPONIBLE'),
        (2, '6666-FFF', 'Ford', 'Focus', 2023, 'GASOLINA', 42.00, 'DISPONIBLE'),
        (3, '7777-GGG', 'Hyundai', 'Tucson', 2024, 'HIBRIDO', 65.00, 'DISPONIBLE'),
        (3, '8888-HHH', 'Nissan', 'Qashqai', 2025, 'HIBRIDO', 70.00, 'DISPONIBLE'),
        (3, '9999-III', 'Peugeot', '3008', 2023, 'DIESEL', 60.00, 'DISPONIBLE'),
        (4, '1010-JJJ', 'Skoda', 'Octavia', 2024, 'DIESEL', 55.00, 'DISPONIBLE'),
        (4, '1111-KKK', 'Ford', 'Mondeo', 2023, 'HIBRIDO', 58.00, 'DISPONIBLE'),
        (4, '1212-LLL', 'Toyota', 'Prius+', 2024, 'HIBRIDO', 62.00, 'DISPONIBLE'),
        (5, '1313-MMM', 'Mercedes', 'Clase E', 2025, 'DIESEL', 120.00, 'DISPONIBLE'),
        (5, '1414-NNN', 'BMW', 'Serie 5', 2025, 'DIESEL', 130.00, 'DISPONIBLE'),
        (5, '1515-OOO', 'Audi', 'A6', 2025, 'DIESEL', 125.00, 'DISPONIBLE')
    ]
    vehicle_map = {}
    for cat, matr, marc, mod, anio, comb, prec, est in vehiculos:
        _ejecutar_sql("INSERT INTO VEHICULOS (id_categoria, matricula, marca, modelo, anio, combustible, precio_dia, estado_vehiculo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [cat, matr, marc, mod, anio, comb, prec, est])
        res = _ejecutar_sql("SELECT id_vehiculo FROM VEHICULOS WHERE matricula = %s", [matr])
        vehicle_map[matr] = res[0][0]

    # 4. Reservas
    res_data = [
        (client_map['23456789B'], vehicle_map['1111-AAA'], '2026-06-01', '2026-06-05', '2026-05-25', 'FINALIZADA'),
        (client_map['12345678A'], vehicle_map['4444-DDD'], '2026-06-10', '2026-06-15', '2026-06-01', 'FINALIZADA'),
        (client_map['12345678Q'], vehicle_map['7777-GGG'], '2026-06-20', '2026-06-25', '2026-06-15', 'FINALIZADA')
    ]
    reserva_ids = []
    for cli_id, veh_id, ini, fin, res_f, est in res_data:
        _ejecutar_sql("""
            INSERT INTO RESERVAS (id_cliente, id_vehiculo, fecha_inicio, fecha_fin, fecha_reserva, estado_reserva)
            VALUES (%s, %s, TO_DATE(%s, 'YYYY-MM-DD'), TO_DATE(%s, 'YYYY-MM-DD'), TO_DATE(%s, 'YYYY-MM-DD'), %s)
        """, [cli_id, veh_id, ini, fin, res_f, est])
        res = _ejecutar_sql("SELECT id_reserva FROM RESERVAS WHERE id_cliente = %s AND id_vehiculo = %s AND fecha_inicio = TO_DATE(%s, 'YYYY-MM-DD')", [cli_id, veh_id, ini])
        reserva_ids.append(res[0][0])

    # 5. Facturas para las 3 reservas baseline (todas finalizadas y pagadas)
    # Reserva 1 (175.00 €)
    _ejecutar_sql("""
        INSERT INTO FACTURAS (id_reserva, fecha_factura, importe_total, estado_pago)
        VALUES (%s, TO_DATE('2026-06-01', 'YYYY-MM-DD'), 175.00, 'PAGADA')
    """, [reserva_ids[0]])
    res = _ejecutar_sql("SELECT id_factura FROM FACTURAS WHERE id_reserva = %s", [reserva_ids[0]])
    fid1 = res[0][0]
    _ejecutar_sql("""
        INSERT INTO PAGOS (id_factura, fecha_pago, importe, metodo_pago)
        VALUES (%s, TO_DATE('2026-06-01', 'YYYY-MM-DD'), 175.00, 'TARJETA')
    """, [fid1])

    # Reserva 2 (225.00 €)
    _ejecutar_sql("""
        INSERT INTO FACTURAS (id_reserva, fecha_factura, importe_total, estado_pago)
        VALUES (%s, TO_DATE('2026-06-10', 'YYYY-MM-DD'), 225.00, 'PAGADA')
    """, [reserva_ids[1]])
    res = _ejecutar_sql("SELECT id_factura FROM FACTURAS WHERE id_reserva = %s", [reserva_ids[1]])
    fid2 = res[0][0]
    _ejecutar_sql("""
        INSERT INTO PAGOS (id_factura, fecha_pago, importe, metodo_pago)
        VALUES (%s, TO_DATE('2026-06-10', 'YYYY-MM-DD'), 225.00, 'TARJETA')
    """, [fid2])

    # Reserva 3 (325.00 €)
    _ejecutar_sql("""
        INSERT INTO FACTURAS (id_reserva, fecha_factura, importe_total, estado_pago)
        VALUES (%s, TO_DATE('2026-06-20', 'YYYY-MM-DD'), 325.00, 'PAGADA')
    """, [reserva_ids[2]])
    res = _ejecutar_sql("SELECT id_factura FROM FACTURAS WHERE id_reserva = %s", [reserva_ids[2]])
    fid3 = res[0][0]
    _ejecutar_sql("""
        INSERT INTO PAGOS (id_factura, fecha_pago, importe, metodo_pago)
        VALUES (%s, TO_DATE('2026-06-20', 'YYYY-MM-DD'), 325.00, 'TRANSFERENCIA')
    """, [fid3])

    # 7. Mantenimientos
    _ejecutar_sql("""
        INSERT INTO MANTENIMIENTOS (id_vehiculo, fecha_mantenimiento, descripcion, coste)
        VALUES (%s, TO_DATE('2026-06-01', 'YYYY-MM-DD'), 'Cambio de aceite', 120.00)
    """, [vehicle_map['1111-AAA']])

    # 8. Incidencias en reserva 2 (reserva_ids[1])
    _ejecutar_sql("""
        INSERT INTO INCIDENCIAS (id_reserva, fecha_incidencia, descripcion, coste, destino_coste, estado_incidencia)
        VALUES (%s, TO_DATE('2026-06-12', 'YYYY-MM-DD'), 'Rotura de espejo lateral', 150.00, 'CLIENTE', 'ABIERTA')
    """, [reserva_ids[1]])

    print("Datos originales cargados exitosamente.")

def generar_datos_adicionales():
    print("Generando datos adicionales coherentes para análisis de tendencias...")
    
    # 1. Crear nuevos clientes (DNI y emails diferentes para no violar UNIQUE)
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
    
    new_cliente_ids = []
    for nom, ape, dni, tel, mail in clientes_data:
        _ejecutar_sql("""
            INSERT INTO CLIENTES (nombre, apellidos, dni, telefono, email)
            VALUES (%s, %s, %s, %s, %s)
        """, [nom, ape, dni, tel, mail])
        res = _ejecutar_sql("SELECT id_cliente FROM CLIENTES WHERE dni = %s", [dni])
        new_cliente_ids.append(res[0][0])

    # 2. Crear nuevos vehículos (con matrículas nuevas)
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
    
    new_vehiculo_ids = []
    vehiculo_precios = {}
    for cat_id, matr, marc, mod, anio, comb, prec, est in vehiculos_data:
        _ejecutar_sql("""
            INSERT INTO VEHICULOS (id_categoria, matricula, marca, modelo, anio, combustible, precio_dia, estado_vehiculo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, [cat_id, matr, marc, mod, anio, comb, prec, est])
        res = _ejecutar_sql("SELECT id_vehiculo FROM VEHICULOS WHERE matricula = %s", [matr])
        vid = res[0][0]
        new_vehiculo_ids.append(vid)
        vehiculo_precios[vid] = prec

    # Obtener precios de vehículos existentes para asociarlos a reservas
    db_vehiculos = _ejecutar_sql("SELECT id_vehiculo, precio_dia FROM VEHICULOS")
    for row in db_vehiculos:
        vehiculo_precios[row[0]] = row[1]

    # 3. Crear Reservas adicionales en un rango temporal amplio (Tendencias)
    hoy = date.today()
    todas_reservas = []
    
    # Seguimiento de reservas por vehículo para evitar solapamientos/dobles reservas
    # Formato: {id_vehiculo: [(fecha_inicio, fecha_fin)]}
    historial_ocupacion = {}
    
    # Inicializar con reservas originales ya cargadas en la BD
    original_reservas = _ejecutar_sql("SELECT id_vehiculo, fecha_inicio, fecha_fin FROM RESERVAS")
    for v_id, f_ini, f_fin in original_reservas:
        # Convertir a objetos date
        d_ini = f_ini.date() if hasattr(f_ini, 'date') else f_ini
        d_fin = f_fin.date() if hasattr(f_fin, 'date') else f_fin
        if v_id not in historial_ocupacion:
            historial_ocupacion[v_id] = []
        historial_ocupacion[v_id].append((d_ini, d_fin))

    # Generar 35 reservas a lo largo de los últimos 6 meses sin solapamientos
    print("Creando 35 reservas adicionales sin solapamiento de fechas para simular historial operativo...")
    target_months = (
        [1] * 5 +   # Enero: 5 reservas
        [2] * 3 +   # Febrero: 3 reservas (temporada baja)
        [3] * 5 +   # Marzo: 5 reservas
        [4] * 9 +   # Abril: 9 reservas (Pico de Semana Santa/Pascua)
        [5] * 5 +   # Mayo: 5 reservas
        [6] * 8     # Junio: 8 reservas (Inicio verano)
    )
    
    dias_mes = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30}
    
    for m in target_months:
        intentos = 0
        success = False
        while not success and intentos < 500:
            intentos += 1
            cid = random.choice(new_cliente_ids)
            vid = random.choice(new_vehiculo_ids)
            
            day = random.randint(1, dias_mes[m])
            ini = date(2026, m, day)
            duracion = random.randint(3, 10)
            fin = ini + timedelta(days=duracion)
            
            # Comprobar solapamiento de fechas
            overlap = False
            if vid in historial_ocupacion:
                for booked_ini, booked_fin in historial_ocupacion[vid]:
                    if ini <= booked_fin and booked_ini <= fin:
                        overlap = True
                        break
            
            if not overlap:
                todas_reservas.append((cid, vid, ini, fin, 'FINALIZADA'))
                if vid not in historial_ocupacion:
                    historial_ocupacion[vid] = []
                historial_ocupacion[vid].append((ini, fin))
                success = True

    # Agregar algunas reservas activas y futuras (sin solapamiento)
    opciones_activas = [
        (new_cliente_ids[4], new_vehiculo_ids[5], hoy - timedelta(days=3), hoy + timedelta(days=4), 'ACTIVA'),
        (new_cliente_ids[5], new_vehiculo_ids[7], hoy - timedelta(days=1), hoy + timedelta(days=6), 'ACTIVA'),
        (new_cliente_ids[6], new_vehiculo_ids[1], hoy + timedelta(days=5), hoy + timedelta(days=12), 'ACTIVA'),
        (new_cliente_ids[7], new_vehiculo_ids[4], hoy + timedelta(days=10), hoy + timedelta(days=15), 'ACTIVA')
    ]
    
    for cid, vid, ini, fin, est in opciones_activas:
        overlap = False
        if vid in historial_ocupacion:
            for booked_ini, booked_fin in historial_ocupacion[vid]:
                if ini <= booked_fin and booked_ini <= fin:
                    overlap = True
                    break
        if not overlap:
            todas_reservas.append((cid, vid, ini, fin, est))
            if vid not in historial_ocupacion:
                historial_ocupacion[vid] = []
            historial_ocupacion[vid].append((ini, fin))

    reserva_ids = []
    reserva_vehiculos = {}
    reserva_dias = {}
    reserva_estados = {}

    for cid, vid, ini, fin, est in todas_reservas:
        fecha_res = ini - timedelta(days=random.randint(2, 10))
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
        
        if res:
            rid = res[0][0]
            reserva_ids.append(rid)
            reserva_vehiculos[rid] = vid
            reserva_estados[rid] = est
            dias = (fin - ini).days
            reserva_dias[rid] = dias if dias > 0 else 1

    # 4. Generar Facturas y Pagos correspondientes
    print("Generando facturas y cobros asociados...")
    for rid in reserva_ids:
        vid = reserva_vehiculos[rid]
        precio = vehiculo_precios[vid]
        dias = reserva_dias[rid]
        importe = precio * dias
        est = reserva_estados[rid]
        
        # Las reservas FINALIZADAS siempre deben estar PAGADAS.
        # Las reservas ACTIVAS pueden tener pago PENDIENTE o PAGADO.
        if est == 'FINALIZADA':
            estado_pago = 'PAGADA'
        else:
            estado_pago = 'PAGADA' if random.random() < 0.60 else 'PENDIENTE'
            
        _ejecutar_sql("""
            INSERT INTO FACTURAS (id_reserva, fecha_factura, importe_total, estado_pago)
            VALUES (%s, SYSDATE - 5, %s, %s)
        """, [rid, importe, estado_pago])
        
        res = _ejecutar_sql("SELECT id_factura FROM FACTURAS WHERE id_reserva = %s", [rid])
        if res:
            fid = res[0][0]
            if estado_pago == 'PAGADA':
                _ejecutar_sql("""
                    INSERT INTO PAGOS (id_factura, fecha_pago, importe, metodo_pago)
                    VALUES (%s, SYSDATE - 4, %s, %s)
                """, [fid, importe, random.choice(['TARJETA', 'EFECTIVO', 'TRANSFERENCIA'])])

    # 5. Crear Incidencias adicionales
    print("Creando incidencias adicionales...")
    if len(reserva_ids) > 5:
        _ejecutar_sql("""
            INSERT INTO INCIDENCIAS (id_reserva, fecha_incidencia, descripcion, coste, destino_coste, estado_incidencia)
            VALUES (%s, SYSDATE - 3, %s, 150.00, 'CLIENTE', 'ABIERTA')
        """, [reserva_ids[0], "Faro delantero izquierdo roto por colisión leve."])
        
        _ejecutar_sql("""
            INSERT INTO INCIDENCIAS (id_reserva, fecha_incidencia, descripcion, coste, destino_coste, estado_incidencia)
            VALUES (%s, SYSDATE - 8, %s, 95.00, 'EMPRESA', 'RESUELTA')
        """, [reserva_ids[1], "Pinchazo en rueda trasera derecha."])
        
        _ejecutar_sql("""
            INSERT INTO INCIDENCIAS (id_reserva, fecha_incidencia, descripcion, coste, destino_coste, estado_incidencia)
            VALUES (%s, SYSDATE - 12, %s, 200.00, 'SEGURO', 'RESUELTA')
        """, [reserva_ids[2], "Golpe en paragolpes trasero."])

    # 6. Crear Mantenimientos adicionales
    print("Creando registros de mantenimiento adicionales...")
    _ejecutar_sql("""
        INSERT INTO MANTENIMIENTOS (id_vehiculo, fecha_mantenimiento, descripcion, coste)
        VALUES (%s, SYSDATE - 15, %s, 180.00)
    """, [new_vehiculo_ids[0], "Cambio de pastillas de freno y discos delanteros."])
    
    _ejecutar_sql("""
        INSERT INTO MANTENIMIENTOS (id_vehiculo, fecha_mantenimiento, descripcion, coste)
        VALUES (%s, SYSDATE - 20, %s, 95.00)
    """, [new_vehiculo_ids[1], "Cambio de neumático tras pinchazo reportado."])

    print("¡Base de datos cargada con éxito con TODOS los datos originales + datos de tendencias!")

if __name__ == '__main__':
    limpiar_tablas()
    cargar_datos_originales_dinamico()
    generar_datos_adicionales()

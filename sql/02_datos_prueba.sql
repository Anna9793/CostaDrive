PROMPT ===== CATEGORIAS =====
INSERT INTO CATEGORIAS_VEHICULO VALUES (
    1,
    'ECONOMICO',
    'Vehículos pequeños y de bajo consumo'
);

INSERT INTO CATEGORIAS_VEHICULO VALUES (
    2,
    'COMPACTO',
    'Vehículos urbanos de tamaño medio'
);

INSERT INTO CATEGORIAS_VEHICULO VALUES (
    3,
    'SUV',
    'Vehículos deportivos utilitarios'
);

INSERT INTO CATEGORIAS_VEHICULO VALUES (
    4,
    'FAMILIAR',
    'Vehículos amplios para familias'
);

INSERT INTO CATEGORIAS_VEHICULO VALUES (
    5,
    'PREMIUM',
    'Vehículos de gama alta'
);

PROMPT ===== CLIENTES =====


INSERT INTO CLIENTES VALUES (1, 'Carlos', 'Sanchez Gómez','23456789B','600222222','carlos@email.com');
INSERT INTO CLIENTES VALUES (2, 'Ana','Martinez González', '12345678A','600111111', 'ana@email.com');
INSERT INTO CLIENTES VALUES (3, 'Alejandro', 'Sánchez Ruiz', '12345678Q', '654123987', 'asanchez@email.com');
INSERT INTO CLIENTES VALUES (4, 'Beatriz', 'Gómez Martín', '87654321W', '698741236', 'bgomez@email.com');
INSERT INTO CLIENTES VALUES (5, 'Javier', 'López Pérez', '11223344E', '612345678', 'jlopez@email.com');
INSERT INTO CLIENTES VALUES (6, 'Lucía', 'Fernández Gil', '99887766R', '678990112', 'lfernandez@email.com');
INSERT INTO CLIENTES VALUES (7, 'Miguel', 'Díaz Castro', '55443322T', '633445566', 'mdiaz@email.com' );
INSERT INTO CLIENTES VALUES (8, 'Elena', 'Ruiz Moreno', '66778899Y', '644556677', 'eruiz@email.com');
INSERT INTO CLIENTES VALUES (9, 'Carlos', 'Jiménez Ruiz', '44332211U', '655667788', 'cjimenez@email.com');
INSERT INTO CLIENTES VALUES (10, 'Sofía', 'Álvarez Navarro', '33221100I', '666778899', 'salvarez@email.com');
INSERT INTO CLIENTES VALUES (11, 'Pablo', 'Moreno Ortiz', '22110099O', '677889900', 'pmoreno@email.com');
INSERT INTO CLIENTES VALUES (12, 'Isabel', 'Vázquez Herrera', '11009988P', '688990011', 'ivazquez@email.com');

PROMPT ===== VEHICULOS =====

-- Categoría 1: ECONOMICO
INSERT INTO VEHICULOS VALUES (1, 1, '1111-AAA', 'Seat', 'Ibiza', 2023, 'GASOLINA', 30.00, 'DISPONIBLE');
INSERT INTO VEHICULOS VALUES (2, 1, '2222-BBB', 'Fiat', '500', 2024, 'GASOLINA', 28.00, 'DISPONIBLE');
INSERT INTO VEHICULOS VALUES (3, 1, '3333-CCC', 'Kia', 'Picanto', 2022, 'GASOLINA', 25.00, 'DISPONIBLE');

-- Categoría 2: COMPACTO
INSERT INTO VEHICULOS VALUES (4, 2, '4444-DDD', 'Volkswagen', 'Golf', 2023, 'HIBRIDO', 45.00, 'DISPONIBLE');
INSERT INTO VEHICULOS VALUES (5, 2, '5555-EEE', 'Toyota', 'Corolla', 2024, 'HIBRIDO', 48.00, 'DISPONIBLE');
INSERT INTO VEHICULOS VALUES (6, 2, '6666-FFF', 'Ford', 'Focus', 2023, 'GASOLINA', 42.00, 'DISPONIBLE');

-- Categoría 3: SUV
INSERT INTO VEHICULOS VALUES (7, 3, '7777-GGG', 'Hyundai', 'Tucson', 2024, 'HIBRIDO', 65.00, 'DISPONIBLE');
INSERT INTO VEHICULOS VALUES (8, 3, '8888-HHH', 'Nissan', 'Qashqai', 2025, 'HIBRIDO', 70.00, 'DISPONIBLE');
INSERT INTO VEHICULOS VALUES (9, 3, '9999-III', 'Peugeot', '3008', 2023, 'DIESEL', 60.00, 'DISPONIBLE');

-- Categoría 4: FAMILIAR
INSERT INTO VEHICULOS VALUES (10, 4, '1010-JJJ', 'Skoda', 'Octavia', 2024, 'DIESEL', 55.00, 'DISPONIBLE');
INSERT INTO VEHICULOS VALUES (11, 4, '1111-KKK', 'Ford', 'Mondeo', 2023, 'HIBRIDO', 58.00, 'DISPONIBLE');
INSERT INTO VEHICULOS VALUES (12, 4, '1212-LLL', 'Toyota', 'Prius+', 2024, 'HIBRIDO', 62.00, 'DISPONIBLE');

-- Categoría 5: PREMIUM
INSERT INTO VEHICULOS VALUES (13, 5, '1313-MMM', 'Mercedes', 'Clase E', 2025, 'DIESEL', 120.00, 'DISPONIBLE');
INSERT INTO VEHICULOS VALUES (14, 5, '1414-NNN', 'BMW', 'Serie 5', 2025, 'DIESEL', 130.00, 'DISPONIBLE');
INSERT INTO VEHICULOS VALUES (15, 5, '1515-OOO', 'Audi', 'A6', 2025, 'DIESEL', 125.00, 'DISPONIBLE');

PROMPT ===== RESERVAS =====
INSERT INTO RESERVAS (
    ID_RESERVA,
    ID_CLIENTE,
    ID_VEHICULO,
    FECHA_INICIO,
    FECHA_FIN,
    ESTADO_RESERVA
)
VALUES (
    1,
    1,
    1,
    DATE '2026-06-10',
    DATE '2026-06-15',
    'FINALIZADA'
);

PROMPT ===== FACTURAS =====

INSERT INTO FACTURAS (
    ID_FACTURA,
    ID_RESERVA,
    IMPORTE_TOTAL,
    ESTADO_PAGO
)
VALUES (
    1,
    1,
    175,
    'PAGADA'
);

PROMPT ===== PAGOS =====

INSERT INTO PAGOS (
    ID_PAGO,
    ID_FACTURA,
    IMPORTE,
    METODO_PAGO
)
VALUES (
    1,
    1,
    175,
    'TARJETA'
);

PROMPT ===== MANTENIMIENTOS =====

INSERT INTO MANTENIMIENTOS (
    ID_MANTENIMIENTO,
    ID_VEHICULO,
    DESCRIPCION,
    COSTE
)
VALUES (
    1,
    1,
    'Cambio de aceite',
    120
);

PROMPT ===== MANTENIMIENTOS =====
INSERT INTO INCIDENCIAS (
    ID_INCIDENCIA,
    ID_RESERVA,
    DESCRIPCION,
    COSTE,
    ESTADO_INCIDENCIA
)
VALUES (
    1,
    1,
    'Arañazo en puerta trasera',
    250,
    'CERRADA'
);

COMMIT;
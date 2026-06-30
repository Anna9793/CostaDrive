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

INSERT INTO CLIENTES (
    ID_CLIENTE,
    NOMBRE,
    APELLIDOS,
    DNI,
    TELEFONO,
    EMAIL
)
VALUES (
    1,
    'Ana',
    'Martinez',
    '12345678A',
    '600111111',
    'ana@email.com'
);

INSERT INTO CLIENTES (
    ID_CLIENTE,
    NOMBRE,
    APELLIDOS,
    DNI,
    TELEFONO,
    EMAIL
)
VALUES (
    2,
    'Carlos',
    'Sanchez',
    '23456789B',
    '600222222',
    'carlos@email.com'
);

PROMPT ===== VEHICULOS =====
INSERT INTO VEHICULOS (
    ID_VEHICULO,
    ID_CATEGORIA,
    MATRICULA,
    MARCA,
    MODELO,
    ANIO,
    COMBUSTIBLE,
    PRECIO_DIA,
    ESTADO_VEHICULO
)
VALUES (
    1,
    1,
    '1234ABC',
    'Seat',
    'Ibiza',
    2022,
    'GASOLINA',
    35,
    'DISPONIBLE'
);

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
CREATE OR REPLACE PROCEDURE CREAR_RESERVA(
    p_id_cliente IN NUMBER,
    p_id_vehiculo IN NUMBER,
    p_fecha_inicio IN DATE,
    p_fecha_fin IN DATE
) IS 
    v_id_reserva NUMBER;
BEGIN

    IF p_fecha_fin <= p_fecha_inicio THEN
        RAISE_APPLICATION_ERROR(-20002, 'La fecha de fin debe ser posterior a la de inicio.');
    END IF;

    IF NOT ESTA_DISPONIBLE(p_id_vehiculo, p_fecha_inicio, p_fecha_fin) THEN
        RAISE_APPLICATION_ERROR(-20003, '¡El coche ya está reservado en estas fechas!');
    END IF;

    INSERT INTO RESERVAS(
        ID_CLIENTE,
        ID_VEHICULO,
        FECHA_INICIO,
        FECHA_FIN,
        FECHA_RESERVA,
        ESTADO_RESERVA
    )
    VALUES (
        p_id_cliente,
        p_id_vehiculo,
        p_fecha_inicio,
        p_fecha_fin,
        SYSDATE,
        'ACTIVA'
    )
    RETURNING ID_RESERVA INTO v_id_reserva;

    -- Generar factura automáticamente
    GENERAR_FACTURA(v_id_reserva);

    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Reserva creada correctamente para el cliente ' || p_id_cliente || '.');
END;
/




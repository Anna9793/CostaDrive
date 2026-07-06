CREATE OR REPLACE PROCEDURE CREAR_RESERVA(
    p_id_cliente IN NUMBER,
    p_id_vehiculo IN NUMBER,
    p_fecha_inicio IN DATE,
    p_fecha_fin IN DATE
) IS 
BEGIN

    IF p_fecha_fin <= p_fecha_inicio THEN
        RAISE_APPLICATION_ERROR(-20002, 'La fecha de fin debe ser posterior a la de inicio.');
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
    );

    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Reserva creada correctamente para el cliente' || p_id_cliente);
END;
/




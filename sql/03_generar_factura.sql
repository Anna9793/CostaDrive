CREATE OR REPLACE PROCEDURE GENERAR_FACTURA (
    p_id_reserva IN NUMBER
) IS 
    v_precio_dia NUMBER;
    v_dias NUMBER;
    v_importe_total NUMBER;
    v_existe NUMBER;

BEGIN
    -- Evitar duplicados
    SELECT COUNT(*) INTO v_existe FROM FACTURAS WHERE ID_RESERVA = p_id_reserva;
    IF v_existe > 0 THEN
        RETURN;
    END IF;

    SELECT(r.FECHA_FIN - r.FECHA_INICIO), v.precio_dia
    INTO v_dias, v_precio_dia
    FROM reservas R
    JOIN VEHICULOS v 
    ON r.ID_VEHICULO = v.ID_VEHICULO
    WHERE r.ID_RESERVA = p_id_reserva;

    v_importe_total := v_dias * v_precio_dia;

    INSERT INTO FACTURAS (ID_RESERVA, FECHA_FACTURA, IMPORTE_TOTAL, ESTADO_PAGO)
    VALUES
    (p_id_reserva, SYSDATE, v_importe_total, 'PENDIENTE');

END;
/



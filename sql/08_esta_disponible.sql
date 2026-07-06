CREATE OR REPLACE FUNCTION ESTA_DISPONIBLE (
    p_id_vehiculo in NUMBER,
    p_fecha_inicio IN DATE,
    p_fecha_fin IN DATE
) RETURN BOOLEAN IS
    v_count NUMBER;

BEGIN
    SELECT COUNT(*)
    INTO v_count
    FROM RESERVAS
    WHERE ID_VEHICULO = p_id_vehiculo
    AND ESTADO_RESERVA = 'ACTIVA'
    AND p_fecha_inicio <= FECHA_FIN
    AND p_fecha_fin >= FECHA_INICIO;

    RETURN v_count = 0;
END;
/
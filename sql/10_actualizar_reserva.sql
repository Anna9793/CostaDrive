CREATE OR REPLACE PROCEDURE SP_ACTUALIZAR_RESERVA (
    p_id_reserva IN NUMBER,
    p_fecha_inicio IN DATE,
    p_fecha_fin IN DATE
) IS
BEGIN
    -- Actualizamos la reserva
    UPDATE RESERVAS 
    SET fecha_inicio = p_fecha_inicio,
        fecha_fin = p_fecha_fin
    WHERE id_reserva = p_id_reserva
    AND estado_reserva != 'CANCELADA'; -- Regla de negocio: no editar si está cancelada

    -- Si no se actualizó ninguna fila, podemos lanzar una excepción personalizada
    IF SQL%ROWCOUNT = 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'La reserva no existe o ya está cancelada.');
    END IF;

END;
/
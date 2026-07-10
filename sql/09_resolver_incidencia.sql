CREATE OR REPLACE PROCEDURE RESOLVER_INCIDENCIA (
    p_id_incidencia IN NUMBER,
    p_coste_final IN NUMBER
) IS
    v_id_reserva NUMBER;
    v_destino VARCHAR2(20);
BEGIN

    SELECT ID_RESERVA, DESTINO_COSTE
    INTO v_id_reserva, v_destino
    FROM INCIDENCIAS
    WHERE ID_INCIDENCIA = p_id_incidencia;

    UPDATE INCIDENCIAS 
    SET ESTADO_INCIDENCIA = 'RESUELTA', 
        COSTE = p_coste_final
    WHERE ID_INCIDENCIA = p_id_incidencia;
    
    IF v_destino = 'EMPRESA' THEN
        INSERT INTO MANTENIMIENTOS(ID_VEHICULO, DESCRIPCION, COSTE)
        SELECT r.ID_VEHICULO, 'Incidencia resuelta (ID: '|| i.id_incidencia ||'): '|| i.DESCRIPCION,
        i.COSTE
        FROM RESERVAS r
        JOIN INCIDENCIAS i ON r.ID_RESERVA = i.ID_RESERVA
        WHERE i.ID_INCIDENCIA = p_id_incidencia;
    END IF;

    COMMIT;

    DBMS_OUTPUT.PUT_LINE('Incidencia ' || p_id_incidencia || ' resuelta y fondos redistribuidos.');

END;
/
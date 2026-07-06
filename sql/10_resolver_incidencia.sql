CREATE OR REPLACE PROCEDURE RESOLVER_INCIDENCIA (
    p_id_incidencia IN NUMBER,
    p_coste_final IN NUMBER
) IS
    v_id_reserva NUMBER;
    v_destino VARCHAR2(20);
BEGIN

    SELECT ID_RESERVA
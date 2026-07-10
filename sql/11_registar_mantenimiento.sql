CREATE OR REPLACE PROCEDURE registrar_mantenimiento(
    p_id_vehiculo IN NUMBER,
    p_desc IN VARCHAR2,
    p_coste IN NUMBER
) AS
BEGIN
    -- 1. Update status
    UPDATE vehiculos SET estado_vehiculo = 'MANTENIMIENTO' WHERE id_vehiculo = p_id_vehiculo;
    
    -- 2. Create record
    INSERT INTO mantenimientos (id_vehiculo, fecha_mantenimiento, descripcion, coste)
    VALUES (p_id_vehiculo, SYSDATE, p_desc, p_coste);
    
    COMMIT; -- Save both as one atomic unit
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK; -- If anything fails, revert everything
        RAISE;
END;
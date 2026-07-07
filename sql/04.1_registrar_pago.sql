CREATE OR REPLACE PROCEDURE REGISTRAR_PAGO (
    p_id_factura IN NUMBER,
    p_metodo IN VARCHAR2,
    p_importe IN NUMBER
) IS
BEGIN
    INSERT INTO PAGOS (id_factura, metodo_pago, importe)
    VALUES (p_id_factura, p_metodo, p_importe);
END;
/
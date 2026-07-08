from django.db import models

import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

class ModelDepartamentos:
    def __init__(self):
        self.connection = oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN")
        )
    
    def get_departamentos_db(self):
        cursor = self.connection.cursor()

        sql = """
        SELECT DEPT_NO, DNOMBRE, LOC
        FROM DEPT
        ORDER BY DEPT_NO
        """
        cursor.execute(sql)

        return cursor.fetchall()
    
    def get_departamento_db(self, deptno):
        cursor = self.connection.cursor()

        sql = """
            SELECT DEPT_NO, DNOMBRE, LOC
            FROM DEPT
            WHERE DEPT_NO = :p
        """

        cursor.execute(sql, [deptno])

        return cursor.fetchone()
    
    def insertar_departamento_db(self, deptno, nombre, loc):
        cursor = self.connection.cursor()

        sql = """
            INSERT INTO DEPT
            VALUES (:p1,:p2,:p3)
        """

        cursor.execute(sql, [deptno, nombre, loc])

        self.connection.commit()

    def modificar_departamento_db(self, deptno, nombre, loc):
        cursor = self.connection.cursor()
        
        sql = """
            UPDATE DEPT
            SET DNOMBRE=:p1,
                LOC=:p2
            WHERE DEPT_NO=:p3
        """
        
        cursor.execute(sql, [nombre, loc, deptno])

        self.connection.commit()

    def eliminar_departamento_db(self, deptno):
        cursor = self.connection.cursor()

        sql = """
        DELETE FROM DEPT
        WHERE DEPT_NO=:p
        """

        cursor.execute(sql, [deptno])

        self.connection.commit()

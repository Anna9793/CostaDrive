import oracledb
import sys

# Forzamos la compatibilidad de tipos para que Django no se queje
oracledb.defaults.fetch_lobs = False
oracledb.version = "8.3.0"
sys.modules["cx_Oracle"] = oracledb

# Esto ayuda a que los tipos de datos de oracledb sean reconocidos por Django
oracledb.Binary = bytes
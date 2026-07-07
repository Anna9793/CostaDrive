import oracledb
import sys

# Forzamos la compatibilidad de tipos para que Django no se queje
oracledb.defaults.fetch_lobs = False
oracledb.version = "8.3.0"
sys.modules["cx_Oracle"] = oracledb
oracledb.Timestamp = datetime.datetime if 'datetime' in globals() else type(None)
oracledb.Binary = bytes
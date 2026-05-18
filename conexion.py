import psycopg2
import os
from dotenv import load_dotenv

# Esto carga las variables del archivo .env a la memoria
load_dotenv() 

def obtener_conexion():
    try:
        conexion = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        return conexion
    except Exception as e:
        print(f"Error al conectar: {e}")
        return None

if __name__ == "__main__":
    conexion_prueba = obtener_conexion()
    if conexion_prueba:
        print("¡Conexión exitosa a PostgreSQL! ")
        conexion_prueba.close()
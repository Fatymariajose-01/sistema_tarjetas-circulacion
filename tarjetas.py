from conexion import obtener_conexion

def consultar_tarjeta(placa):
    conexion = obtener_conexion()
    if not conexion:
        return {"error": "No se pudo conectar a la base de datos"}

    try:
        cursor = conexion.cursor()
        
        # El cambio clave está en la última línea: WHERE ... t.estado != 'Reemplazada'
        sql = """
            SELECT 
                t.id_tarjeta, t.estado,
                v.marca, v.modelo, v.color, v.numero_motor, 
                p.nombre AS propietario,
                c.estado AS calcomania_pagada
            FROM Tarjeta_Circulacion t
            JOIN Vehiculo v ON t.placa = v.placa
            JOIN Propietario p ON t.id_propietario = p.id_propietario
            LEFT JOIN Calcomania c ON v.placa = c.placa AND c.anio = EXTRACT(YEAR FROM CURRENT_DATE)
            WHERE t.placa = %s AND t.estado != 'Reemplazada'
        """
        cursor.execute(sql, (placa,))
        resultado = cursor.fetchone()

        if resultado:
            return {
                "id_tarjeta": resultado[0],
                "estado_tarjeta": resultado[1], # <--- Aquí ahora viajará "Inactiva (Impago)"
                "marca": resultado[2],
                "modelo": resultado[3],
                "color": resultado[4],
                "motor": resultado[5],       
                "propietario": resultado[6], 
                "solvente": resultado[7]     
            }
        else:
            return {"mensaje": "No se encontró información para esta placa."}

    except Exception as e:
        return {"error": f"Error en la consulta: {e}"}
    
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
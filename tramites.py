from conexion import obtener_conexion
from datetime import date

def ejecutar_sql(sql, parametros):
    """Función auxiliar para evitar repetir código de conexión"""
    conexion = obtener_conexion()
    if not conexion: return False, "Error de conexion"
    try:
        cursor = conexion.cursor()
        cursor.execute(sql, parametros)
        conexion.commit()
        return True, "Operacion exitosa"
    except Exception as e:
        conexion.rollback()
        return False, str(e)
    finally:
        if conexion: conexion.close()

def registrar_cambio_dueno(placa, nuevo_propietario_id, empleado_id):
    # Esta ya la tenías, el Trigger en Postgres hace el trabajo pesado
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        hoy = date.today()
        # Insertar nueva tarjeta (dispara el trigger)
        sql = "INSERT INTO Tarjeta_Circulacion (placa, id_propietario, fecha_emision, fecha_vencimiento, estado) VALUES (%s, %s, %s, %s, 'Activa')"
        cursor.execute(sql, (placa, nuevo_propietario_id, hoy, date(hoy.year + 1, hoy.month, hoy.day)))
        # Registro legal
        cursor.execute("INSERT INTO Tramite (tipo_tramite, fecha_tramite, descripcion, placa, id_usuario) VALUES ('Traspaso', %s, %s, %s, %s)",
                       (hoy, f"Nuevo dueno: {nuevo_propietario_id}", placa, empleado_id))
        conexion.commit()
        return True, "Traspaso procesado e historial actualizado"
    except Exception as e:
        conexion.rollback()
        return False, str(e)
    finally: conexion.close()

def actualizar_vehiculo(placa, campo, nuevo_valor, empleado_id):
    """Mantenimiento: Cambio de Motor o Color"""
    tipo = "Cambio de Motor" if campo == "numero_motor" else "Cambio de Color"
    sql_v = f"UPDATE Vehiculo SET {campo} = %s WHERE placa = %s"
    sql_t = "INSERT INTO Tramite (tipo_tramite, fecha_tramite, descripcion, placa, id_usuario) VALUES (%s, CURRENT_DATE, %s, %s, %s)"
    
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(sql_v, (nuevo_valor, placa))
        cursor.execute(sql_t, (tipo, f"Nuevo valor: {nuevo_valor}", placa, empleado_id))
        conexion.commit()
        return True, f"{tipo} registrado correctamente"
    except Exception as e:
        conexion.rollback()
        return False, str(e)
    finally: conexion.close()

def cambiar_estado_tarjeta(placa, motivo, empleado_id):
    """Desactivación de tarjeta guardando el motivo específico."""
    
    # Aquí unimos la palabra con el motivo que escribiste (ej. "Inactiva (Impago)")
    estado_con_motivo = f"Inactiva ({motivo})" 

    sql_t = "UPDATE Tarjeta_Circulacion SET estado = %s WHERE placa = %s AND estado = 'Activa'"
    sql_log = "INSERT INTO Tramite (tipo_tramite, fecha_tramite, descripcion, placa, id_usuario) VALUES ('Baja', CURRENT_DATE, %s, %s, %s)"
    
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        
        # 1. Actualizamos el estado de la tarjeta con el motivo
        cursor.execute(sql_t, (estado_con_motivo, placa))
        
        # 2. Guardamos el historial en Tramites
        cursor.execute(sql_log, (f"Desactivación por {motivo}", placa, empleado_id))
        
        conexion.commit()
        return True, f"Tarjeta inactivada exitosamente por {motivo}."
    except Exception as e:
        conexion.rollback()
        return False, str(e)
    finally:
        if conexion: conexion.close()
def emitir_primera_tarjeta(placa, vin, motor, marca, modelo, linea, color, anio, dpi_propietario, empleado_id):
    """Inscribe un vehículo nuevo y le genera su primera tarjeta de circulación."""
    conexion = obtener_conexion()
    if not conexion: 
        return False, "Error de conexión."
    try:
        cursor = conexion.cursor()
        hoy = date.today()
        # Se asume 1 año de vigencia a partir de hoy
        vencimiento = date(hoy.year + 1, hoy.month, hoy.day) 

        # 1. Crear el vehículo en la base de datos
        sql_vehiculo = """
            INSERT INTO Vehiculo (placa, vin, numero_motor, marca, modelo, linea, color, anio) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_vehiculo, (placa, vin, motor, marca, modelo, linea, color, anio))

        # 2. Crear su primera tarjeta
        sql_tarjeta = """
            INSERT INTO Tarjeta_Circulacion (placa, id_propietario, fecha_emision, fecha_vencimiento, estado) 
            VALUES (%s, %s, %s, %s, 'Activa')
        """
        cursor.execute(sql_tarjeta, (placa, dpi_propietario, hoy, vencimiento))

        # 3. Guardar constancia en Trámites
        sql_tramite = """
            INSERT INTO Tramite (tipo_tramite, fecha_tramite, descripcion, placa, id_usuario) 
            VALUES ('Primera Emision', %s, %s, %s, %s)
        """
        cursor.execute(sql_tramite, (hoy, f"Inscripcion a DPI: {dpi_propietario}", placa, empleado_id))

        # Confirmar todo
        conexion.commit()
        return True, "¡Vehículo inscrito y nueva tarjeta generada con éxito!"
        
    except Exception as e:
        conexion.rollback()
        return False, f"Error al emitir tarjeta: {e}"
    finally:
        if conexion: 
            conexion.close()
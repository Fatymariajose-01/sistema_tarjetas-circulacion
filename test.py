from tarjetas import consultar_tarjeta
from tramites import registrar_cambio_dueno

def menu_pruebas():
    while True:
        print("\n" + "="*35)
        print("🚗 SISTEMA DE TARJETAS (MODO PRUEBA)")
        print("="*35)
        print("1. Consultar Tarjeta de Circulación")
        print("2. Registrar Traspaso (Cambio de Dueño)")
        print("3. Salir")
        print("-" * 35)
        
        opcion = input("Elige una opción (1/2/3): ")

        if opcion == '1':
            placa = input("\nIngresa el número de placa a buscar (ej. P-001ABC): ")
            print("\nBuscando en la base de datos...")
            resultado = consultar_tarjeta(placa)
            print("-" * 35)
            print(resultado)

        elif opcion == '2':
            print("\n--- NUEVO TRASPASO ---")
            placa = input("Ingresa la placa del vehículo: ")
            nuevo_propietario = input("Ingresa el DPI/NIT del nuevo dueño: ")
            # Usamos el id_usuario 1 simulando que el empleado con ID 1 está usando el sistema
            empleado_id = 1 
            
            print("\nProcesando el trámite y actualizando historial...")
            exito, mensaje = registrar_cambio_dueno(placa, nuevo_propietario, empleado_id)
            print("-" * 35)
            print(mensaje)

        elif opcion == '3':
            print("\nSaliendo de las pruebas... ¡Hasta luego!")
            break
            
        else:
            print("\n❌ Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    menu_pruebas()
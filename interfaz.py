import customtkinter as ctk
from tarjetas import consultar_tarjeta
import tramites 

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SistemaTarjetas(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Tránsito")
        self.geometry("800x650")
        self.rol_actual = ""
        self.mostrar_pantalla_login()

    def mostrar_pantalla_login(self):
        self.frame_login = ctk.CTkFrame(self)
        self.frame_login.pack(pady=100, padx=200, fill="both", expand=True)
        ctk.CTkLabel(self.frame_login, text="Inicio de Sesión", font=("Arial", 24, "bold")).pack(pady=20)
        self.txt_usuario = ctk.CTkEntry(self.frame_login, placeholder_text="Usuario (admin/super/operador)", width=250)
        self.txt_usuario.pack(pady=10)
        ctk.CTkButton(self.frame_login, text="Ingresar", command=self.verificar_credenciales).pack(pady=20)

    def verificar_credenciales(self):
        u = self.txt_usuario.get().lower().strip()
        if u == "admin": self.rol_actual = "Administrador"
        elif u == "super": self.rol_actual = "Supervisor"
        elif u == "operador": self.rol_actual = "Operador"
        else:
            print("Usuario no reconocido.")
            return
        
        self.frame_login.destroy()
        self.mostrar_pantalla_principal()

    def mostrar_pantalla_principal(self):
        self.tabview = ctk.CTkTabview(self, width=750, height=550)
        self.tabview.pack(pady=20, padx=20)

        # 1. Tab Consulta
        tab_c = self.tabview.add("Consulta")
        self.construir_modulo_consulta(tab_c)

        # 2. Tabs Administrativos
        if self.rol_actual in ["Supervisor", "Administrador"]:
            tab_t = self.tabview.add("Trámites (Mantenimiento)")
            self.construir_modulo_tramites(tab_t)
            
            tab_n = self.tabview.add("Nueva Tarjeta")
            self.construir_modulo_nueva_tarjeta(tab_n)

    def construir_modulo_consulta(self, contenedor):
        marco = ctk.CTkFrame(contenedor, fg_color="transparent")
        marco.pack(pady=10)
        self.ent_placa_c = ctk.CTkEntry(marco, placeholder_text="Ingrese Placa", width=200)
        self.ent_placa_c.grid(row=0, column=0, padx=10)
        ctk.CTkButton(marco, text="Consultar", command=self.ejecutar_consulta).grid(row=0, column=1)
        self.res_c = ctk.CTkTextbox(contenedor, width=650, height=350, font=("Arial", 14))
        self.res_c.pack(pady=10)
        self.res_c.configure(state="disabled")

    def construir_modulo_tramites(self, contenedor):
        ctk.CTkLabel(contenedor, text="Mantenimiento y Baja de Tarjetas", font=("Arial", 18, "bold")).pack(pady=10)
        self.ent_placa_t = ctk.CTkEntry(contenedor, placeholder_text="Número de Placa (Ej. P-123ABC)", width=350)
        self.ent_placa_t.pack(pady=5)
        self.ent_valor_t = ctk.CTkEntry(contenedor, placeholder_text="Nuevo Valor (DPI, Color o Motor)", width=350)
        self.ent_valor_t.pack(pady=5)
        ctk.CTkLabel(contenedor, text="Seleccione el tipo de trámite:").pack(pady=5)
        self.opt_tramite = ctk.CTkSegmentedButton(contenedor, values=["Traspaso", "Color", "Motor", "Inactivar"])
        self.opt_tramite.pack(pady=10)
        self.opt_tramite.set("Traspaso")
        ctk.CTkButton(contenedor, text="Procesar Trámite", fg_color="green", hover_color="darkgreen", command=self.procesar_tramite_click).pack(pady=20)

    def construir_modulo_nueva_tarjeta(self, contenedor):
        ctk.CTkLabel(contenedor, text="Inscripción de Vehículo y Emisión", font=("Arial", 18, "bold")).pack(pady=10)
        
        marco_form = ctk.CTkFrame(contenedor, fg_color="transparent")
        marco_form.pack(pady=5)

        # Matriz de cajas de texto
        self.nt_placa = ctk.CTkEntry(marco_form, placeholder_text="Placa (P-XXX)", width=170)
        self.nt_placa.grid(row=0, column=0, padx=5, pady=5)
        self.nt_dpi = ctk.CTkEntry(marco_form, placeholder_text="DPI del Dueño", width=170)
        self.nt_dpi.grid(row=0, column=1, padx=5, pady=5)

        self.nt_vin = ctk.CTkEntry(marco_form, placeholder_text="Número VIN", width=170)
        self.nt_vin.grid(row=1, column=0, padx=5, pady=5)
        self.nt_motor = ctk.CTkEntry(marco_form, placeholder_text="Número de Motor", width=170)
        self.nt_motor.grid(row=1, column=1, padx=5, pady=5)

        self.nt_marca = ctk.CTkEntry(marco_form, placeholder_text="Marca", width=170)
        self.nt_marca.grid(row=2, column=0, padx=5, pady=5)
        self.nt_modelo = ctk.CTkEntry(marco_form, placeholder_text="Modelo", width=170)
        self.nt_modelo.grid(row=2, column=1, padx=5, pady=5)

        self.nt_linea = ctk.CTkEntry(marco_form, placeholder_text="Línea (Ej. Sedán)", width=170)
        self.nt_linea.grid(row=3, column=0, padx=5, pady=5)
        self.nt_color = ctk.CTkEntry(marco_form, placeholder_text="Color", width=170)
        self.nt_color.grid(row=3, column=1, padx=5, pady=5)

        self.nt_anio = ctk.CTkEntry(marco_form, placeholder_text="Año (Ej. 2026)", width=170)
        self.nt_anio.grid(row=4, column=0, columnspan=2, pady=5)

        ctk.CTkButton(contenedor, text="Guardar y Emitir", command=self.generar_nueva_tarjeta_click).pack(pady=15)

    # --- FUNCIONES ---
    def ejecutar_consulta(self):
        placa = self.ent_placa_c.get().strip().upper()
        if not placa: return
        res = consultar_tarjeta(placa)
        
        texto_final = ""
        if "error" in res: texto_final = f"Ocurrió un error: {res['error']}"
        elif "mensaje" in res: texto_final = f"Aviso: {res['mensaje']}"
        else:
            estado_calc = "Solvente" if res.get('solvente') else "En Mora"
            texto_final = (
                f"DATOS DE LA TARJETA\n{'-'*40}\n"
                f"No. Tarjeta: {res.get('id_tarjeta', 'N/A')} ({res.get('estado_tarjeta', 'N/A')})\n"
                f"Propietario: {res.get('propietario', 'N/A')}\n\n"
                f"DATOS DEL VEHÍCULO\n{'-'*40}\n"
                f"Marca y Modelo: {res.get('marca', '')} {res.get('modelo', '')}\n"
                f"Color: {res.get('color', '')}\n"
                f"Motor: {res.get('motor', 'N/A')}\n"
                f"Calcomanía Anual: {estado_calc}\n"
            )
        
        self.res_c.configure(state="normal")
        self.res_c.delete("0.0", "end")
        self.res_c.insert("0.0", texto_final)
        self.res_c.configure(state="disabled")

    def procesar_tramite_click(self):
        placa = self.ent_placa_t.get().strip().upper()
        valor = self.ent_valor_t.get().strip()
        tipo = self.opt_tramite.get()
        emp_id = 1 

        if not placa:
            print("Error: Ingrese placa.")
            return
            
        # Modificamos la validación para exigir el motivo de la baja
        if not valor:
            if tipo == "Inactivar":
                print("Error: Debe escribir el motivo de la inactivación (Impago o Vencimiento).")
            else:
                print("Error: Ingrese nuevo valor.")
            return

        if tipo == "Traspaso": 
            exito, msg = tramites.registrar_cambio_dueno(placa, valor, emp_id)
        elif tipo == "Color": 
            exito, msg = tramites.actualizar_vehiculo(placa, "color", valor, emp_id)
        elif tipo == "Motor": 
            exito, msg = tramites.actualizar_vehiculo(placa, "numero_motor", valor, emp_id)
        elif tipo == "Inactivar": 
            # Ahora pasamos el texto que el usuario escribió (Impago o Vencimiento) como el motivo
            exito, msg = tramites.cambiar_estado_tarjeta(placa, valor, emp_id)
        
        print(f"Trámite: {msg}") 
        self.ent_placa_t.delete(0, 'end')
        self.ent_valor_t.delete(0, 'end')

    def generar_nueva_tarjeta_click(self):
        placa = self.nt_placa.get().strip().upper()
        dpi = self.nt_dpi.get().strip()
        vin = self.nt_vin.get().strip().upper()
        motor = self.nt_motor.get().strip().upper()
        marca = self.nt_marca.get().strip().capitalize()
        modelo = self.nt_modelo.get().strip().capitalize()
        linea = self.nt_linea.get().strip().capitalize()
        color = self.nt_color.get().strip().capitalize()
        anio_texto = self.nt_anio.get().strip()
        emp_id = 1

        # Validación simple
        if not all([placa, dpi, vin, motor, marca, modelo, linea, color, anio_texto]):
            print("Error: Todos los campos son obligatorios.")
            return
            
        try:
            anio = int(anio_texto)
        except ValueError:
            print("Error: El año debe ser un número entero.")
            return

        exito, msg = tramites.emitir_primera_tarjeta(placa, vin, motor, marca, modelo, linea, color, anio, dpi, emp_id)
        print(f"Nueva Tarjeta: {msg}")
        
        # Limpiar campos si tuvo éxito
        if exito:
            for entry in [self.nt_placa, self.nt_dpi, self.nt_vin, self.nt_motor, self.nt_marca, self.nt_modelo, self.nt_linea, self.nt_color, self.nt_anio]:
                entry.delete(0, 'end')

if __name__ == "__main__":
    app = SistemaTarjetas()
    app.mainloop()
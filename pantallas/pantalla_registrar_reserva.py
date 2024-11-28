import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from services.reserva_service import ReservaService
from pantallas.helpers.window_size_helper import WindowSizeHelper
from PIL import Image
from tkcalendar import Calendar
from datetime import datetime

class RegistrarReserva(ctk.CTkToplevel):
    def __init__(self, db):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.db = db
        self.reserva_service = None
        try:
            self.reserva_service = ReservaService(db)
        except Exception as e:
            messagebox.showerror("Error", f"Error al inicializar el servicio de reservas: {e}")
            self.destroy()  # Cierra la ventana si no se puede inicializar el servicio
            return

        self.title('Registrar Reserva')

        # Tamaño y configuración de la ventana
        self.geometry("1100x800")
        self.minsize(1100, 800)
        self.maxsize(1100, 800)

        self.tamanio_fuente = 14
        self.fuente = "Arial"
        self.width = 250

        # Crear widgets con estilo y valores por defecto
        self.crear_widgets()

    def crear_widgets(self):
        try:
            # Frame principal con padding adicional para una apariencia más espaciosa
            frame = ctk.CTkFrame(self, corner_radius=10)
            frame.pack(fill="both", expand=True, padx=30, pady=30)

            # Titulo
            ctk.CTkLabel(frame, text='Registrar Reserva', font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=20)

            # Etiquetas y campos de entrada

            # Combo Cliente
            ctk.CTkLabel(frame, text="Cliente:", font=(self.fuente, self.tamanio_fuente)).grid(row=1, column=0, padx=10, pady=10)
            self.combo_cliente = ctk.CTkComboBox(frame, values=["Cliente 1", "Cliente 2", "Cliente 3"], width=self.width, font=(self.fuente, self.tamanio_fuente))
            self.combo_cliente.grid(row=1, column=1, padx=10, pady=10)
            self.combo_cliente.set("Seleccione un cliente")

            # Combo Habitacion
            ctk.CTkLabel(frame, text="Habitación:", font=(self.fuente, self.tamanio_fuente)).grid(row=2, column=0, padx=10, pady=10)
            self.combo_habitacion = ctk.CTkComboBox(frame, values=["101 - Simple", "102 - Doble", "103 - Suite"], width=self.width, font=(self.fuente, self.tamanio_fuente))
            self.combo_habitacion.grid(row=2, column=1, padx=10, pady=10)
            self.combo_habitacion.set("Seleccione una habitación")

            # Fecha Entrada
            ctk.CTkLabel(frame, text="Fecha de Entrada (dd/mm/YYYY):", font=(self.fuente, self.tamanio_fuente)).grid(row=3, column=0, rowspan=2, padx=10, pady=10)
            self.entry_fecha_entrada = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamanio_fuente))
            self.entry_fecha_entrada.insert(0, self.fecha_actual())
            self.entry_fecha_entrada.grid(row=3, column=1, padx=10, pady=10)
            self.open_calendar_fecha_entrada = ctk.CTkButton(frame, text="Seleccionar Fecha", command=lambda: self.open_calendar("fecha_entrada"))
            self.open_calendar_fecha_entrada.grid(row=4, column=1, padx=10, pady=10)

            # Fecha Salida
            ctk.CTkLabel(frame, text="Fecha de Salida (dd/mm/YYYY):", font=(self.fuente, self.tamanio_fuente)).grid(row=5, column=0, rowspan=2, padx=10, pady=10)
            self.entry_fecha_salida = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamanio_fuente))
            self.entry_fecha_salida.grid(row=5, column=1, padx=10, pady=10)

            self.open_calendar_fecha_salida = ctk.CTkButton(frame, text="Seleccionar Fecha", command=lambda: self.open_calendar("fecha_salida"))
            self.open_calendar_fecha_salida.grid(row=6, column=1, padx=10, pady=10)

            # Cantidad de Personas
            ctk.CTkLabel(frame, text="Cantidad de Personas:", font=(self.fuente, self.tamanio_fuente)).grid(row=7, column=0, padx=10, pady=10)
            self.entry_cantidad_personas = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamanio_fuente))
            self.entry_cantidad_personas.grid(row=7, column=1, padx=10, pady=10)

            # Botón para registrar reserva
            ctk.CTkButton(frame, text="Registrar Reserva", command=self.registrar_reserva).grid(row=8, column=0, columnspan=2, pady=10)

            # Tabla para mostrar las reservas registradas
            self.tabla_reservas = ttk.Treeview(frame, columns=("id_reserva", "cliente", "habitacion", "fecha_entrada", "fecha_salida", "cantidad_personas"), show="headings")
            self.tabla_reservas.heading("id_reserva", text="ID Reserva")
            self.tabla_reservas.heading("cliente", text="Cliente")
            self.tabla_reservas.heading("habitacion", text="Habitación")
            self.tabla_reservas.heading("fecha_entrada", text="Fecha de Entrada")
            self.tabla_reservas.heading("fecha_salida", text="Fecha de Salida")
            self.tabla_reservas.heading("cantidad_personas", text="Personas")
            self.tabla_reservas.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

            # asignar tamaño a cada columna
            self.tabla_reservas.column("id_reserva", width=100)
            self.tabla_reservas.column("cliente", width=250)
            self.tabla_reservas.column("habitacion", width=250)
            self.tabla_reservas.column("fecha_entrada", width=150)
            self.tabla_reservas.column("fecha_salida", width=150)
            self.tabla_reservas.column("cantidad_personas", width=90)

            self.update_idletasks()
            self.after(5, lambda: WindowSizeHelper.centrar_ventana(self))

            self.actualizar_tabla()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al cargar la interfaz: {e}")
            self.destroy()  # Cerrar la ventana si ocurre un error en la carga de los widgets

    def open_calendar(self, tipo_fecha):
        try:
            top = tk.Toplevel(self)
            top.grab_set()

            top.title("Seleccionar Fecha")
            cal = Calendar(top, selectmode='day', date_pattern='dd/mm/yyyy')
            cal.pack(pady=20)

            select_button = ttk.Button(top, text="Confirmar", command=lambda: self.select_date(cal, top, tipo_fecha))
            select_button.pack()

        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir el calendario: {e}")

    def select_date(self, cal, top, tipo_fecha):
        fecha_seleccionada = cal.get_date()
        if tipo_fecha == "fecha_entrada":
            self.entry_fecha_entrada.delete(0, tk.END)
            self.entry_fecha_entrada.insert(0, fecha_seleccionada)
        elif tipo_fecha == "fecha_salida":
            self.entry_fecha_salida.delete(0, tk.END)
            self.entry_fecha_salida.insert(0, fecha_seleccionada)
        top.destroy()

    def fecha_actual(self):
        return datetime.now().strftime("%d/%m/%Y")

    def registrar_reserva(self):
        try:
            cliente_id = self.combo_cliente.get()
            habitacion_nro = self.combo_habitacion.get().split(" - ")[0]
            fecha_entrada = self.entry_fecha_entrada.get()
            fecha_salida = self.entry_fecha_salida.get()
            cantidad_personas = self.entry_cantidad_personas.get()

            # Validaciones
            if not cliente_id or not habitacion_nro or not fecha_entrada or not fecha_salida or not cantidad_personas:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            # Verificación de fechas
            fecha_entrada = datetime.strptime(fecha_entrada, "%d/%m/%Y")
            fecha_salida = datetime.strptime(fecha_salida, "%d/%m/%Y")
            if fecha_salida <= fecha_entrada:
                messagebox.showerror("Error", "La fecha de salida debe ser posterior a la de entrada.")
                return

            # Verificación de capacidad
            if habitacion_nro == "103" and int(cantidad_personas) > 4:
                messagebox.showerror("Error", "La Suite solo admite hasta 4 personas.")
                return

            # Guardar la reserva
            reserva = {
                "cliente_id": cliente_id,
                "habitacion_nro": habitacion_nro,
                "fecha_entrada": fecha_entrada,
                "fecha_salida": fecha_salida,
                "cantidad_personas": cantidad_personas
            }

            self.reserva_service.registrar_reserva(reserva)
            messagebox.showinfo("Reserva Registrada", "La reserva ha sido registrada exitosamente")
            self.actualizar_tabla()

        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar la reserva: {e}")

    def actualizar_tabla(self):
        try:
            # Limpiar tabla antes de actualizar
            for row in self.tabla_reservas.get_children():
                self.tabla_reservas.delete(row)

            # Obtener las reservas desde el servicio
            reservas = self.reserva_service.obtener_reservas()

            # Insertar las reservas en la tabla
            for reserva in reservas:
                self.tabla_reservas.insert("", "end", values=(
                    reserva["id_reserva"],
                    reserva["cliente_nombre"],
                    f"{reserva['habitacion_nro']} - {reserva['habitacion_tipo']}",
                    reserva["fecha_entrada"],
                    reserva["fecha_salida"],
                    reserva["cantidad_personas"]
                ))

        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar la tabla: {e}")

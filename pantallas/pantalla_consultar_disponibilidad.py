from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry, Calendar  # Importar DateEntry
import customtkinter as ctk
from datetime import datetime

from pantallas.helpers.window_size_helper import WindowSizeHelper
from services.habitacion_service import HabitacionService
from services.reserva_service import ReservaService


class ConsultarDisponibilidad(ctk.CTkToplevel):
    def __init__(self, db):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.db = db
        self.title('Consultar Disponibilidad Habitaciones')

        # Tamaño y configuración de la ventana
        self.geometry("1100x800")  # Ajustar el tamaño
        self.minsize(1100, 800)

        self.tamanio_fuente = 14
        self.fuente = "Arial"
        self.width = 250

        self.habitacion_service = HabitacionService(db)
        self.reserva_service = ReservaService(db)

        self.habitaciones = self.habitacion_service.get_all()

        # Crear widgets con estilo y valores por defecto
        self.crear_widgets()

    def crear_widgets(self):
        # Frame principal con padding adicional para una apariencia más espaciosa
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Titulo
        ctk.CTkLabel(frame, text='Consultar Disponibilidad Habitaciones', font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=20)


        self.combo_habitacion = ctk.CTkComboBox(frame,
                                                values=[f"{habitacion.numero} - {habitacion.tipo}" for habitacion in
                                                        self.habitaciones]
                                                , width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.combo_habitacion.grid(row=1, column=1, padx=10, pady=10)
        self.combo_habitacion.set("Seleccione una habitación")

        ctk.CTkLabel(frame, text="Fecha de Inicio (dd/mm/YYYY):",
                     font=(self.fuente, self.tamanio_fuente)
                     ).grid(row=1, column=0, padx=10, pady=10)

        self.entry_fecha_inicio = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.entry_fecha_inicio.insert(0, self.fecha_actual())
        self.entry_fecha_inicio.grid(row=1, column=1, padx=10, pady=10)
        self.open_calendar_fecha_inicio = ctk.CTkButton(frame, text="Seleccionar Fecha",
                                                        command=lambda: self.open_calendar("fecha_entrada"))
        self.open_calendar_fecha_inicio.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame, text="Fecha de Salida (dd/mm/YYYY):",
                     font=(self.fuente, self.tamanio_fuente)).grid(row=3, column=0, rowspan=1, padx=10, pady=10)
        self.entry_fecha_fin = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.entry_fecha_fin.grid(row=3, column=1, padx=10, pady=10)

        self.open_calendar_fecha_fin = ctk.CTkButton(frame, text="Seleccionar Fecha",
                                                     command=lambda: self.open_calendar("fecha_salida"))
        self.open_calendar_fecha_fin.grid(row=4, column=1, padx=10, pady=10)

        # Tabla para mostrar las habitaciones disponibles
        self.tabla_habitaciones = ttk.Treeview(frame, columns=("numero", "tipo", "estado", "precio_por_noche"),
                                               show="headings")

        # Configurar los encabezados de la tabla
        self.tabla_habitaciones.heading("numero", text="Número")
        self.tabla_habitaciones.heading("tipo", text="Tipo")
        self.tabla_habitaciones.heading("estado", text="Estado")
        self.tabla_habitaciones.heading("precio_por_noche", text="Precio por Noche")

        # Asignar tamaño a cada columna
        self.tabla_habitaciones.column("numero", width=100)
        self.tabla_habitaciones.column("tipo", width=150)
        self.tabla_habitaciones.column("estado", width=100)
        self.tabla_habitaciones.column("precio_por_noche", width=150)

        # Botón para buscar reserva
        ctk.CTkButton(frame, text="Buscar Habitaciones", command=self.buscar_habitaciones_disponibles).grid(row=6, column=0,
                                                                                        columnspan=2, pady=25)

        # Mostrar la tabla en el grid
        self.tabla_habitaciones.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def fecha_actual(self):
        return datetime.now().strftime("%d/%m/%Y")

    def open_calendar(self, tipo_fecha):
        top = Toplevel(self)
        top.grab_set()

        top.title("Seleccionar Fecha")
        cal = Calendar(top, selectmode='day', date_pattern='dd/mm/yyyy')
        cal.pack(pady=20)

        select_button = ttk.Button(top, text="Confirmar", command=lambda: self.select_date(cal, top, tipo_fecha))
        select_button.pack(pady=10)

        top.update_idletasks()
        WindowSizeHelper.centrar_ventana(top)

    def select_date(self, cal, top, tipo_fecha):
        if tipo_fecha == "fecha_entrada":
            self.entry_fecha_inicio.delete(0, "end")
            self.entry_fecha_inicio.insert(0, cal.get_date())
        else:
            self.entry_fecha_fin.delete(0, "end")
            self.entry_fecha_fin.insert(0, cal.get_date())
        top.destroy()

    def buscar_habitaciones_disponibles(self):
        fecha_inicio = self.entry_fecha_inicio.get()
        fecha_fin = self.entry_fecha_fin.get()

        # Validar que las fechas no estén vacías
        if not fecha_inicio or not fecha_fin:
            messagebox.showerror("Error", "Debe ingresar ambas fechas.")
            return

        try:
            # Convertir las fechas ingresadas a objetos datetime
            fecha_inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y")
            fecha_fin = datetime.strptime(fecha_fin, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "El formato de la fecha debe ser dd/mm/yyyy.")
            return

        # Validar que la fecha de inicio sea menor o igual a la fecha de fin
        if fecha_inicio > fecha_fin:
            messagebox.showerror("Error", "La fecha de inicio debe ser menor o igual a la fecha de salida.")
            return

        # Llamar al servicio para obtener las habitaciones disponibles
        habitaciones_disponibles = self.habitacion_service.get_habitaciones_disponibles_by_date_range(fecha_inicio, fecha_fin)

        if len(habitaciones_disponibles) == 0:
            messagebox.showinfo("No hay habitaciones disponibles", "No se encontraron habitaciones disponibles entre las fechas solicitadas")

        print("Cantidad de habitaciones disponibles:", len(habitaciones_disponibles))

        # Limpiar la tabla antes de insertar los nuevos resultados
        self.tabla_habitaciones.delete(*self.tabla_habitaciones.get_children())

        # Insertar las habitaciones disponibles en la tabla
        for habitacion in habitaciones_disponibles:
            self.tabla_habitaciones.insert("", "end", values=(habitacion.numero, habitacion.tipo, habitacion.estado, habitacion.precio_por_noche))

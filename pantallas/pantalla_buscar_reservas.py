import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from pantallas.helpers.window_size_helper import WindowSizeHelper
import customtkinter as ctk
from datetime import datetime

from services.cliente_service import ClienteService
from services.habitacion_service import HabitacionService
from services.reserva_service import ReservaService


class BuscarReservas(ctk.CTkToplevel):
    def __init__(self, db):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.db = db
        self.title('Buscar Reservas')

        # Tamaño y configuracion de la ventana
        self.geometry("1100x800")  # Ajustar el tamaño
        self.minsize(1100, 800)

        self.tamanio_fuente = 14
        self.fuente = "Arial"
        self.width = 250

        self.habitacion_service = HabitacionService(db)
        self.cliente_service = ClienteService(db)
        self.reserva_service = ReservaService(db)

        self.clientes = self.cliente_service.get_all()
        self.habitaciones = self.habitacion_service.get_all()
        self.crear_widgets()

    def crear_widgets(self):
        # Frame principal con padding adicional para una apariencia más espaciosa
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Titulo
        ctk.CTkLabel(frame, text='Buscar Reservas', font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=20)

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

        # Botón para buscar reserva
        ctk.CTkButton(frame, text="Buscar Reservas", command=self.buscar_reservas).grid(row=5, column=0,
                                                                                            columnspan=2, pady=25)
        # Tabla para mostrar las reservas registradas
        self.tabla_reservas = ttk.Treeview(frame, columns=(
            "id_reserva", "cliente", "habitacion", "fecha_entrada", "fecha_salida", "cantidad_personas"),
                                           show="headings")
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

        # self.limpiar_campos()
        # self.actualizar_tabla()

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

    def fecha_actual(self):
        return datetime.now().strftime("%d/%m/%Y")

    def limpiar_campos(self):
        # self.entry_fecha_inicio.insert(0, "")
        # self.entry_fecha_fin.delete(0, "end")
        # self.actualizar_tabla()
        pass

    def buscar_reservas(self):
        fecha_inicio = self.entry_fecha_inicio.get()
        fecha_fin = self.entry_fecha_fin.get()

        # Convertir las fechas a formato yyyy-mm-dd
        fecha_inicio = datetime.strptime(fecha_inicio, '%d/%m/%Y').strftime('%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin, '%d/%m/%Y').strftime('%Y-%m-%d')

        if fecha_inicio == "" or fecha_fin == "":
            messagebox.showerror("Error", "Debe ingresar una fecha.")
            return
        elif fecha_inicio > fecha_fin:
            messagebox.showerror("Error", "La fecha de inicio debe ser menor a la fecha de salida.")
            return

        reservas_filtradas = self.reserva_service.get_reservas_by_date_range(fecha_inicio, fecha_fin)

        self.cargar_tabla(reservas_filtradas)
        self.limpiar_campos()
        # Mostrar un mensaje si no se encontraron reservas
        if not reservas_filtradas:
            messagebox.showinfo("Resultado", "No se encontraron reservas en el rango de fechas seleccionado.")

    def cargar_tabla(self, reservas):
        # Limpiar la tabla antes de cargar nuevos datos
        for row in self.tabla_reservas.get_children():
            self.tabla_reservas.delete(row)

        # Cargar los datos de las reservas en la tabla
        for reserva in reservas:
            cliente = self.cliente_service.get_by_id(reserva.cliente)
            habitacion = self.habitacion_service.get_by_id(reserva.habitacion)
            self.tabla_reservas.insert(
                "", "end", values=(
                    reserva.id_reserva,
                    f"{cliente.nombre} {cliente.apellido}",
                    f"{habitacion.numero} - {habitacion.tipo}",
                    reserva.fecha_entrada,
                    reserva.fecha_salida,
                    reserva.cantidad_personas
                )
            )
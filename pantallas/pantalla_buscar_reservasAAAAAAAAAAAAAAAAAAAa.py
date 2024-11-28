import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import customtkinter as ctk
from datetime import datetime
from PIL import Image, ImageTk

from pantallas.helpers.window_size_helper import WindowSizeHelper
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

        # Tamaño y configuración de la ventana
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
        # Fondo con imagen
        self.fondo_imagen = Image.open("recursos/foto_logo.jpg")
        self.fondo_imagen = self.fondo_imagen.resize((1100, 800), Image.LANCZOS)
        self.fondo_imagen = ImageTk.PhotoImage(self.fondo_imagen)

        fondo_label = tk.Label(self, image=self.fondo_imagen)
        fondo_label.place(relwidth=1, relheight=1)

        # Frame central donde se coloca todo el contenido
        frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent", width=800, height=600)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Titulo
        ctk.CTkLabel(frame, text='Buscar Reservas', font=("Arial", 18), text_color="white").grid(row=0, column=0,
                                                                                                 columnspan=2, pady=20)

        ctk.CTkLabel(frame, text="Fecha de Inicio (dd/mm/YYYY):", font=(self.fuente, self.tamanio_fuente),
                     text_color="white").grid(row=1, column=0, padx=10, pady=10)

        self.entry_fecha_inicio = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamanio_fuente), state="readonly")
        self.entry_fecha_inicio.insert(0, self.fecha_actual())
        self.entry_fecha_inicio.grid(row=1, column=1, padx=10, pady=10)

        self.open_calendar_fecha_inicio = ctk.CTkButton(frame, text="Seleccionar Fecha",
                                                        command=lambda: self.open_calendar("fecha_entrada"))
        self.open_calendar_fecha_inicio.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame, text="Fecha de Salida (dd/mm/YYYY):", font=(self.fuente, self.tamanio_fuente),
                     text_color="white").grid(row=3, column=0, rowspan=1, padx=10, pady=10)

        self.entry_fecha_fin = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamanio_fuente), state="readonly")
        self.entry_fecha_fin.grid(row=3, column=1, padx=10, pady=10)

        self.open_calendar_fecha_fin = ctk.CTkButton(frame, text="Seleccionar Fecha",
                                                     command=lambda: self.open_calendar("fecha_salida"))
        self.open_calendar_fecha_fin.grid(row=4, column=1, padx=10, pady=10)

        # Botón para buscar reservas
        ctk.CTkButton(frame, text="Buscar Reservas", command=self.buscar_reservas).grid(row=5, column=0, columnspan=2,
                                                                                        pady=25)

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

        # Asignar tamaño a cada columna
        self.tabla_reservas.column("id_reserva", width=100)
        self.tabla_reservas.column("cliente", width=250)
        self.tabla_reservas.column("habitacion", width=250)
        self.tabla_reservas.column("fecha_entrada", width=150)
        self.tabla_reservas.column("fecha_salida", width=150)
        self.tabla_reservas.column("cantidad_personas", width=90)

        # Botón de Volver
        boton_volver = ctk.CTkButton(self, text="Volver", command=self.volver, font=("Arial", 14), fg_color="gray",
                                     text_color="white", hover_color="#A9A9A9")
        boton_volver.place(relx=0.5, rely=0.95, anchor="center", y=-30)

        self.update_idletasks()
        self.after(5, lambda: WindowSizeHelper.centrar_ventana(self))

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
            self.entry_fecha_inicio.configure(state="normal")
            self.entry_fecha_inicio.delete(0, "end")
            self.entry_fecha_inicio.insert(0, cal.get_date())
            self.entry_fecha_inicio.configure(state="readonly")
        else:
            self.entry_fecha_fin.configure(state="normal")
            self.entry_fecha_fin.delete(0, "end")
            self.entry_fecha_fin.insert(0, cal.get_date())
            self.entry_fecha_fin.configure(state="readonly")
        top.destroy()

    def fecha_actual(self):
        return datetime.now().strftime("%d/%m/%Y")

    def limpiar_campos(self):
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

        if not reservas_filtradas:
            messagebox.showinfo("Resultado", "No se encontraron reservas en el rango de fechas seleccionado.")

    def cargar_tabla(self, reservas):
        for row in self.tabla_reservas.get_children():
            self.tabla_reservas.delete(row)

        for reserva in reservas:
            cliente = self.cliente_service.get_by_id(reserva.cliente)
            habitacion = self.habitacion_service.get_by_id(reserva.habitacion)
            self.tabla_reservas.insert("", "end", values=(
                reserva.id_reserva,
                f"{cliente.nombre} {cliente.apellido}",
                f"{habitacion.numero} - {habitacion.tipo}",
                reserva.fecha_entrada,
                reserva.fecha_salida,
                reserva.cantidad_personas
            ))

    def volver(self):
        self.destroy()


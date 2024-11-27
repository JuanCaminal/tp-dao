from tkinter import *
from tkcalendar import Calendar
from datetime import datetime
from pantallas.helpers.window_size_helper import WindowSizeHelper
import customtkinter as ctk
from PIL import Image
from tkinter import ttk, messagebox
from services.habitacion_service import HabitacionService
from services.cliente_service import ClienteService
from services.reserva_service import ReservaService


class RegistrarReserva(ctk.CTkToplevel):
    def __init__(self, db, pantalla_principal):
        super().__init__()
        self.fuente = None
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.db = db
        self.pantalla_principal = pantalla_principal
        self.reserva_service = ReservaService(db)  # Asegúrate de que exista un servicio para manejar reservas
        self.title('Registrar Reserva')

        # Fijar el tamaño de la ventana
        self.geometry("1100x800")  # Tamaño de ventana ajustado a 1100x800
        self.resizable(False, False)  # Tamaño fijo

        # Configurar fondo
        self.configurar_fondo()

        # Crear widgets
        self.crear_widgets()

    def configurar_fondo(self):
        background_image = ctk.CTkImage(
            Image.open("recursos/foto_fondo.jpg"),
            size=(1100, 800)
        )
        self.bg_label = ctk.CTkLabel(self, image=background_image, text="")
        self.bg_label.place(relwidth=1, relheight=1)

    def crear_widgets(self):
        # Frame principal
        frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#162447")  # Fondo personalizado
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Título principal
        ctk.CTkLabel(frame, text='Registrar Reserva', font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2,
                                                                                       pady=20)

        # Campos para cliente
        ctk.CTkLabel(frame, text="Cliente:", font=(self.fuente, self.tamanio_fuente)).grid(row=1, column=0, padx=10,
                                                                                           pady=10)
        self.combo_cliente = ctk.CTkComboBox(frame,
                                             values=[f"{cliente.nombre} {cliente.apellido}" for cliente in
                                                     self.clientes],
                                             width=self.width, font=(self.fuente, self.tamanio_fuente),
                                             state='readonly')
        self.combo_cliente.grid(row=1, column=1, padx=10, pady=10)
        self.combo_cliente.set("Seleccione un cliente")

        # Campos para habitación
        ctk.CTkLabel(frame, text="Habitación:", font=(self.fuente, self.tamanio_fuente)).grid(row=2, column=0, padx=10,
                                                                                              pady=10)
        self.combo_habitacion = ctk.CTkComboBox(frame,
                                                values=[f"{habitacion.numero} - {habitacion.tipo}" for habitacion in
                                                        self.habitaciones],
                                                width=self.width, font=(self.fuente, self.tamanio_fuente),
                                                state='readonly')
        self.combo_habitacion.grid(row=2, column=1, padx=10, pady=10)
        self.combo_habitacion.set("Seleccione una habitación")

        # Campos para fechas
        self._crear_campo_fecha(frame, "Fecha de Entrada (dd/mm/YYYY):", 3, "fecha_entrada")
        self._crear_campo_fecha(frame, "Fecha de Salida (dd/mm/YYYY):", 5, "fecha_salida")

        # Campo para cantidad de personas
        ctk.CTkLabel(frame, text="Cantidad de Personas:", font=(self.fuente, self.tamanio_fuente)).grid(row=7, column=0,
                                                                                                        padx=10,
                                                                                                        pady=10)
        self.entry_cantidad_personas = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.entry_cantidad_personas.grid(row=7, column=1, padx=10, pady=10)

        # Botón para registrar la reserva
        ctk.CTkButton(frame, text="Registrar Reserva", command=self.registrar_reserva).grid(row=8, column=0,
                                                                                            columnspan=2, pady=20)

        # Tabla para mostrar reservas registradas
        self._crear_tabla_reservas(frame)

        # Centrar ventana
        self.update_idletasks()
        self.after(5, lambda: WindowSizeHelper.centrar_ventana(self))
        self.actualizar_tabla()

    def _crear_campo_fecha(self, frame, texto, fila, tipo_fecha):
        """Método auxiliar para crear campos de fecha con un botón para seleccionar desde un calendario."""
        ctk.CTkLabel(frame, text=texto, font=(self.fuente, self.tamanio_fuente)).grid(row=fila, column=0, padx=10,
                                                                                      pady=10)
        entry = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamanio_fuente))
        entry.insert(0, self.fecha_actual())
        entry.grid(row=fila, column=1, padx=10, pady=10)

        ctk.CTkButton(frame, text="Seleccionar Fecha", command=lambda: self.open_calendar(tipo_fecha)).grid(
            row=fila + 1, column=1, padx=10, pady=10)

        setattr(self, f"entry_{tipo_fecha}", entry)

    def _crear_tabla_reservas(self, frame):
        """Crea y configura la tabla para mostrar reservas registradas."""
        self.tabla_reservas = ttk.Treeview(frame, columns=(
        "id_reserva", "cliente", "habitacion", "fecha_entrada", "fecha_salida", "cantidad_personas"), show="headings")
        self.tabla_reservas.grid(row=9, column=0, columnspan=2, padx=10, pady=20)

        # Configuración de encabezados
        headers = [("id_reserva", "ID Reserva", 100),
                   ("cliente", "Cliente", 250),
                   ("habitacion", "Habitación", 250),
                   ("fecha_entrada", "Fecha de Entrada", 150),
                   ("fecha_salida", "Fecha de Salida", 150),
                   ("cantidad_personas", "Personas", 100)]

        for col, text, width in headers:
            self.tabla_reservas.heading(col, text=text)
            self.tabla_reservas.column(col, width=width)

    # Resto de los métodos (sin cambios en lógica)
    def open_calendar(self, tipo_fecha):
        """Abre un calendario para seleccionar una fecha."""
        top = Toplevel(self)
        top.grab_set()
        top.title("Seleccionar Fecha")
        cal = Calendar(top, selectmode='day', date_pattern='dd/mm/yyyy')
        cal.pack(pady=20)
        ttk.Button(top, text="Confirmar", command=lambda: self.select_date(cal, top, tipo_fecha)).pack(pady=10)

        WindowSizeHelper.centrar_ventana(top)

    def fecha_actual(self):
        """Devuelve la fecha actual en formato dd/mm/YYYY."""
        return datetime.now().strftime("%d/%m/%Y")

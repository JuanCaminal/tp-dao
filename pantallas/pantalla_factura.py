import customtkinter as ctk

from services.cliente_service import ClienteService
from services.factura_service import FacturaService
from services.habitacion_service import HabitacionService
from services.reserva_service import ReservaService

"""
Unica pantalla que no se llego a completar
"""
class EmitirFactura(ctk.CTkToplevel):
    def __init__(self, db):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.db = db
        self.title('Registrar Reserva')

        # Tamaño y configuración de la ventana
        self.geometry("1100x800")  # Ajustar el tamaño
        self.minsize(1100, 800)
        self.maxsize(1100,800)

        self.tamanio_fuente = 14
        self.fuente = "Arial"
        self.width = 250

        self.habitacion_service = HabitacionService(db)
        self.factura_service = FacturaService(db)
        self.cliente_service = ClienteService(db)
        self.reserva_service = ReservaService(db)

        self.clientes = self.cliente_service.get_all()
        self.reservas = self.reserva_service.get_all()
        self.habitaciones = self.habitacion_service.get_all()

        # Crear widgets con estilo y valores por defecto
        self.crear_widgets()

    def crear_widgets(self):
        # Frame principal con padding adicional para una apariencia más espaciosa
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Titulo
        ctk.CTkLabel(frame, text='Emitir factura', font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=20)

        # Etiquetas y campos de entrada

        # Combo Clientes
        ctk.CTkLabel(frame, text="Cliente:",
                     font=(self.fuente, self.tamanio_fuente)
                     ).grid(row=1, column=0, padx=10, pady=10)
        self.combo_cliente = ctk.CTkComboBox(frame, values=[f"{cliente.id_cliente} - {cliente.nombre} {cliente.apellido}" for cliente in
                                                            self.clientes]
                                             , width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.combo_cliente.grid(row=1, column=1, padx=10, pady=10)
        self.combo_cliente.set("Seleccione un cliente")

        datos_cliente = self.combo_cliente.get()

        if datos_cliente != "Seleccione un cliente":
            datos_cliente = datos_cliente.split(" - ")
            id_cliente = datos_cliente[0]


        # Combo Habitacion
        ctk.CTkLabel(frame, text="Habitación:",
                     font=(self.fuente, self.tamanio_fuente,)
                     ).grid(row=2, column=0, padx=10, pady=10)
        self.combo_habitacion = ctk.CTkComboBox(frame,
                                                values=[f"{habitacion.numero} - {habitacion.tipo}" for habitacion in
                                                        self.habitaciones]
                                                , width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.combo_habitacion.grid(row=2, column=1, padx=10, pady=10)
        self.combo_habitacion.set("Seleccione una habitación")


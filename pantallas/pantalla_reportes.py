import customtkinter as ctk

from pantallas.pantalla_asignar_empleado import AsignarEmpleadoXHabitacion
from pantallas.pantalla_buscar_reservas import BuscarReservas
from pantallas.pantalla_registrar_cliente import RegistrarCliente
from pantallas.pantalla_consultar_disponibilidad import ConsultarDisponibilidad
from pantallas.pantalla_habitacion import RegistrarHabitacion
from pantallas.pantalla_registrar_reserva import RegistrarReserva

from pantallas.helpers.window_size_helper import WindowSizeHelper
from services.reporte_service import ReporteService


class PantallaReportes(ctk.CTkToplevel):
    def __init__(self, db):
        super().__init__()

        self.db = db

        self.reporte_service = ReporteService(db)

        self.title("Reportes")

        # Configuración de tema oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Remover el tamaño fijo, permitiendo que se ajuste al contenido
        self.resizable(True, True)

        # Etiqueta de bienvenida
        label = ctk.CTkLabel(self, text=" -  Seleccione el reporte que desea generar  - ",
                             font=ctk.CTkFont(size=18, weight="bold"))
        label.pack(pady=(30, 20))  # Añadir espacio superior para centrar mejor

        # Crear un frame para organizar los botones con mayor separación
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=30, padx=30)

        # Botones del menú
        botones = [
            ("Listar Reservas", self.abrir_reporte_reservas),
            ("Ingresos por habitaciones", self.abrir_registrar_cliente),
            ("Ocupacion Promedio", self.abrir_reporte_ocupacion_promedio),
        ]

        for texto, comando in botones:
            boton = ctk.CTkButton(button_frame, text=texto, command=comando, width=300, height=40, font=ctk.CTkFont(size=16))
            boton.pack(pady=10)  # Separación entre botones

        # Actualizar la ventana para que se ajuste al contenido
        self.update_idletasks()

        # Centrar la ventana después del renderizado completo
        self.after(10, lambda: WindowSizeHelper.centrar_ventana(self))

    # Métodos para abrir las otras pantallas
    def abrir_reporte_reservas(self):
        buscar_reservas = BuscarReservas(self.db)
        buscar_reservas.grab_set()

    def abrir_registrar_cliente(self):
        registrar_cliente = RegistrarCliente(self.db)
        registrar_cliente.grab_set()

    def abrir_reporte_ocupacion_promedio(self):
        """Llama al servicio para generar el reporte de ocupación promedio."""
        self.reporte_service.generar_reporte_ocupacion_promedio()
        print("Reporte de ocupación promedio generado con éxito")
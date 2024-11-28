import customtkinter as ctk
from PIL import Image

from pantallas.pantalla_asignar_empleado import AsignarEmpleadoXHabitacion
from pantallas.pantalla_buscar_reservasAAAAAAAAAAAAAAAAAAAa import BuscarReservas
from pantallas.pantalla_factura import EmitirFactura
from pantallas.pantalla_registrar_cliente import RegistrarCliente
from pantallas.pantalla_consultar_disponibilidad import ConsultarDisponibilidad
from pantallas.pantalla_habitacion import RegistrarHabitacion
from pantallas.pantalla_registrar_reserva import RegistrarReserva
from pantallas.pantalla_check_in_out import CheckInOut
from pantallas.helpers.window_size_helper import WindowSizeHelper
from pantallas.pantalla_reportes import PantallaReportes
from pantallas.pantalla_gestion_eventos import RegistrarEvento


class PantallaPrincipal(ctk.CTk):
    def __init__(self, db):
        super().__init__()

        self.db = db
        self.title("Menú Principal - Sistema de Gestión de Hotel")

        # Configurar ventana inicial con resolución fija
        self.geometry("1800x1000")
        self.minsize(1800, 1000)
        self.resizable(True, True)

        # Configuración de tema oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Configurar fondo utilizando CTkImage
        background_image = ctk.CTkImage(
            Image.open("recursos/foto_fondo.jpg"),
            size=(1800, 1000)
        )
        bg_label = ctk.CTkLabel(self, image=background_image, text="")
        bg_label.place(relwidth=1, relheight=1)

        # Reemplazar título con imagen
        title_image = ctk.CTkImage(
            Image.open("recursos/foto_logo.jpg"),  # Reemplaza con la ruta correcta
            size=(150, 150 )  # Ajusta el tamaño si es necesario
        )
        title_label = ctk.CTkLabel(self, image=title_image, text="")
        title_label.pack(pady=(30, 20))  # Espaciado superior/inferior

        # Etiqueta de bienvenida
        label = ctk.CTkLabel(
            self, text=" Bienvenido al Sistema de Gestión de Hotel Royal ",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="white",
            fg_color="transparent"  # Sin fondo
        )
        label.pack(pady=(30, 20))

        # Frame transparente para botones
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=30, padx=30, fill="none", expand=True)

        # Botones del menú
        botones = [
            ("Registrar Habitación", self.abrir_registrar_habitacion, "white", "#3a3a3a"),
            ("Registrar Cliente", self.abrir_registrar_cliente, "white", "#3a3a3a"),
            ("Registrar Reserva", self.abrir_registrar_reserva, "white", "#3a3a3a"),
            ("Check In/Out", self.abrir_check_in_out, "white", "#3a3a3a"),
            ("Registrar Eventos", self.abrir_gestion_eventos, "white", "#3a3a3a"),
            ("Asignar Empleados a habitación", self.abrir_asignar_empleado, "white", "#3a3a3a"),
            ("Consultar Disponibilidad de habitaciones", self.abrir_consultar_disponibilidad_habitaciones, "white", "#3a3a3a"),
            ("Generar Reportes", self.generar_reportes, "white", "#3a3a3a"),
            ("Salir", self.quit, "white", "#8B0000"),  # Rojo para el botón de salir
        ]

        for texto, comando, text_color, hover_color in botones:
            boton = ctk.CTkButton(
                button_frame, text=texto, command=comando,
                font=ctk.CTkFont(size=16),
                fg_color="transparent",  # Sin fondo
                text_color=text_color,
                hover_color=hover_color,
                corner_radius=10, height=50, width=400
            )
            boton.pack(pady=15)  # Espaciado entre botones

        # Ajustar automáticamente la imagen de fondo al tamaño de la ventana
        self.bind("<Configure>", lambda e: self.adjust_background(background_image))

        # Centrar la ventana
        self.after(10, lambda: WindowSizeHelper.centrar_ventana(self))

    def adjust_background(self, bg_image):
        """Reajustar la imagen de fondo según el tamaño de la ventana."""
        width = self.winfo_width()
        height = self.winfo_height()
        bg_image.configure(size=(width, height))

    # Métodos para abrir las otras pantallas
    def abrir_registrar_habitacion(self):
        registrar_habitacion = RegistrarHabitacion(self.db)
        registrar_habitacion.grab_set()

    def abrir_registrar_cliente(self):
        registrar_cliente = RegistrarCliente(self.db, self)  # Agrega "self" como pantalla_principal
        registrar_cliente.grab_set()

    def abrir_registrar_reserva(self):
        registrar_reserva = RegistrarReserva(self.db, self)
        registrar_reserva.grab_set()

    def abrir_check_in_out(self):
        check_in_out = CheckInOut(self.db)
        check_in_out.grab_set()

    def abrir_gestion_eventos(self):
        check_in_out = RegistrarEvento(self.db,self)
        check_in_out.grab_set()

    def abrir_asignar_empleado(self):
        asignar_empleado_x_habitacion = AsignarEmpleadoXHabitacion(self.db)
        asignar_empleado_x_habitacion.grab_set()

    def abrir_consultar_disponibilidad_habitaciones(self):
        consultar_disponibilidad = ConsultarDisponibilidad(self.db)
        consultar_disponibilidad.grab_set()

    def generar_reportes(self):
        generar_reportes = PantallaReportes(self.db)
        generar_reportes.grab_set()

    def quit(self):
        self.db.close_db()
        super().quit()


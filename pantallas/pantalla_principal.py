import customtkinter as ctk

from pantallas.pantalla_asignar_empleado import AsignarEmpleadoXHabitacion
from pantallas.pantalla_buscar_reservas import BuscarReservas
from pantallas.pantalla_factura import EmitirFactura
from pantallas.pantalla_registrar_cliente import RegistrarCliente
from pantallas.pantalla_consultar_disponibilidad import ConsultarDisponibilidad
from pantallas.pantalla_habitacion import RegistrarHabitacion
from pantallas.pantalla_registrar_reserva import RegistrarReserva

from pantallas.helpers.window_size_helper import WindowSizeHelper
from pantallas.pantalla_reportes import PantallaReportes


class PantallaPrincipal(ctk.CTk):
    def __init__(self, db):
        super().__init__()

        self.db = db
        self.title("Menú Principal - Sistema de Gestión de Hotel")

        # Pantalla programando actualmente
        # registrar_factura = EmitirFactura(self.db)
        # registrar_factura.grab_set()

        WindowSizeHelper.set_size(self, 1150, 800)  # Definir el tamaño inicial
        self.minsize(650, 800)
        self.maxsize(650, 800)

        # Configuración de tema oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Remover el tamaño fijo, permitiendo que se ajuste al contenido
        self.resizable(True, True)

        # Etiqueta de bienvenida
        label = ctk.CTkLabel(self, text=" -  Bienvenido al Sistema de Gestión de Hotel  - ", font=ctk.CTkFont(size=18, weight="bold"))
        label.pack(pady=(30, 20))  # Añadir espacio superior para centrar mejor

        # Crear un frame para organizar los botones con mayor separación
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=30, padx=30)


        # Botones del menú
        botones = [
            ("Registrar Habitación", self.abrir_registrar_habitacion),
            ("Registrar Cliente", self.abrir_registrar_cliente),
            ("Registrar Reserva", self.abrir_registrar_reserva),
            ("Registrar Factura", self.abrir_registrar_factura),
            ("Asignar Empleados a habitación", self.abrir_asignar_empleado),
            ("Consultar Disponibilidad de habitaciones", self.abrir_consultar_disponibilidad_habitaciones),
            ("Generar Reportes", self.generar_reportes),
            ("Salir", self.quit)
        ]

        for texto, comando in botones:
            boton = ctk.CTkButton(button_frame, text=texto, command=comando, width=300, height=40, font=ctk.CTkFont(size=16))
            boton.pack(pady=10)  # Separación entre botones

        # Actualizar la ventana para que se ajuste al contenido
        self.update_idletasks()

        # Centrar la ventana después del renderizado completo
        self.after(10, lambda: WindowSizeHelper.centrar_ventana(self))

    # Métodos para abrir las otras pantallas
    def abrir_registrar_habitacion(self):
        registrar_habitacion = RegistrarHabitacion(self.db)
        registrar_habitacion.grab_set()

    def abrir_registrar_cliente(self):
        registrar_cliente = RegistrarCliente(self.db)
        registrar_cliente.grab_set()

    def abrir_registrar_reserva(self):
        registrar_reserva = RegistrarReserva(self.db)
        registrar_reserva.grab_set()


    def abrir_registrar_factura(self):
        registrar_factura = EmitirFactura(self.db)
        registrar_factura.grab_set()

    def abrir_asignar_empleado(self):
        asignar_empleado_x_habitacion = AsignarEmpleadoXHabitacion(self.db)
        asignar_empleado_x_habitacion.grab_set()

    def abrir_consultar_disponibilidad_habitaciones(self):
        consultar_disponibilidad = ConsultarDisponibilidad(self.db)
        consultar_disponibilidad.grab_set()

    def generar_reportes(self):
        generar_reportes = PantallaReportes(self.db)
        generar_reportes.grab_set()
        # generar_reportes.mainloop()

    def quit(self):
        self.db.close_db()
        super().quit()

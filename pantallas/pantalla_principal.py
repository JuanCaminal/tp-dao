import customtkinter as ctk
from pantallas.pantalla_cliente import RegistrarCliente
from pantallas.pantalla_habitacion import RegistrarHabitacion
from pantallas.pantalla_reserva import RegistrarReserva

# from views.consultar_autos_vendidos import ConsultarAutosVendidos
# from views.consultar_servicios_realizados import ConsultarServiciosRealizados
# from views.registrar_auto import RegistrarAuto
# from views.helpers.window_size_helper import WindowSizeHelper
# from views.registrar_cliente import RegistrarCliente
# from views.registrar_vendedor import RegistrarVendedor
# from views.registrar_venta import RegistrarVenta
# from views.registrar_servicio import RegistrarServicio
# from views.generar_reportes import GenerarReportes
# from views.gestion_inventario import GestionInventario
from pantallas.helpers.window_size_helper import WindowSizeHelper


class PantallaPrincipal(ctk.CTk):
    def __init__(self, db):
        super().__init__()

        self.db = db
        self.title("Menú Principal - Sistema de Gestión de Hotel")

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
            ("Registrar Factura", self.abrir_registrar_vendedor),
            ("Asignar Empleados a habitación", self.abrir_registrar_servicio),
            ("Consultar Disponibilidad de habitaciones", self.consultar_autos_vendidos),
            ("Consultar Servicios", self.consultar_servicios),
            ("Consultar Servicios", self.consultar_servicios),
            ("Generar Reportes", self.generar_reportes),
            ("Gestión de Inventario", self.abrir_gestion_inventario),
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

    def abrir_registrar_vendedor(self):
        pass

    def abrir_registrar_servicio(self):
        pass
        
    def consultar_autos_vendidos(self):
        pass
        
    def consultar_servicios(self):
        pass

    def generar_reportes(self):
        pass

    def abrir_gestion_inventario(self):
        pass

    def quit(self):
        self.db.close_db()
        super().quit()

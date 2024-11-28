import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk  # Para manejar imágenes de fondo

from pantallas.pantalla_buscar_reservas import BuscarReservas

from pantallas.pantalla_asignar_empleado import AsignarEmpleadoXHabitacion
from pantallas.pantalla_buscar_reservasAAAAAAAAAAAAAAAAAAAa import BuscarReservas
from pantallas.pantalla_registrar_cliente import RegistrarCliente
from pantallas.pantalla_consultar_disponibilidad import ConsultarDisponibilidad
from pantallas.pantalla_habitacion import RegistrarHabitacion
from pantallas.pantalla_registrar_reserva import RegistrarReserva

from pantallas.helpers.window_size_helper import WindowSizeHelper
from services.reporte_service import ReporteService
from reportes.reporte_ocupacion_promedio import generar_reporte_ocupacion_promedio


class PantallaReportes(ctk.CTkToplevel):
    def __init__(self, db):
        super().__init__()

        self.db = db
        self.reporte_service = ReporteService(db)

        self.title("Reportes")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Establecer tamaño fijo
        self.geometry("1000x700")  # Tamaño fijo más grande
        self.resizable(False, False)

        # Cargar imagen de fondo
        self.bg_image = ctk.CTkImage(Image.open("recursos/foto_fondo.jpg"), size=(1000, 700))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image)
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        # Frame principal con transparencia para ver el fondo
        main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Etiqueta de bienvenida
        label = ctk.CTkLabel(main_frame, text=" -  Seleccione el reporte que desea generar  - ",
                             font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=(30, 20))

        # Crear un frame para organizar los botones con mayor separación
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=30, padx=30)

        # Botones del menú
        botones = [
            ("Listar Reservas", self.abrir_reporte_reservas),
            ("Ingresos por habitaciones", self.generar_reporte_ingresos_por_habitaciones),
            ("Ocupación Promedio", self.generar_reporte_ocupacion_promedio),
        ]

        for texto, comando in botones:
            boton = ctk.CTkButton(button_frame, text=texto, command=comando, width=400, height=50,
                                  font=ctk.CTkFont(size=18))
            boton.pack(pady=15)

        # Botón de volver
        boton_volver = ctk.CTkButton(main_frame, text="Volver", command=self.destroy, width=400, height=50,
                                     font=ctk.CTkFont(size=18))
        boton_volver.pack(pady=20)

        # Centrar la ventana después del renderizado completo
        self.after(10, lambda: WindowSizeHelper.centrar_ventana(self))

    # Métodos para abrir las otras pantallas
    def abrir_reporte_reservas(self):
        buscar_reservas = BuscarReservas(self.db)
        buscar_reservas.grab_set()

    def generar_reporte_ingresos_por_habitaciones(self):
        try:
            self.reporte_service.generar_reporte_ingresos_por_habitaciones()
            messagebox.showinfo("Reporte exitoso", "Reporte de Ingresos por habitaciones generado con éxito")
        except Exception as e:
            messagebox.showerror('Error', f'No se pudo generar el reporte: {e}')

    def generar_reporte_ocupacion_promedio(self):
        """Llama al servicio para generar el reporte de ocupación promedio."""
        try:
            generar_reporte_ocupacion_promedio(self, tipo='Simple', estado='ocupada')
            messagebox.showinfo("Reporte exitoso", "Reporte de ocupación promedio generado con éxito")
        except Exception as e:
            messagebox.showerror('Error', f'No se pudo generar el reporte: {e}')

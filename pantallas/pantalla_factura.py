import customtkinter as ctk

from services.factura_service import FacturaService


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

        self.tamanio_fuente = 14
        self.fuente = "Arial"
        self.width = 250

        self.factura_service = FacturaService(db)

        # Crear widgets con estilo y valores por defecto
        self.crear_widgets()

    def crear_widgets(self):
        # Frame principal con padding adicional para una apariencia más espaciosa
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Titulo
        ctk.CTkLabel(frame, text='Emitir factura', font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=20)


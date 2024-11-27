import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from services.habitacion_service import HabitacionService
from pantallas.helpers.window_size_helper import WindowSizeHelper
from PIL import Image

class RegistrarHabitacion(ctk.CTkToplevel):
    def __init__(self, db):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.db = db
        self.habitacion_service = HabitacionService(db)
        self.title('Registrar Habitación')

        # Tamaño y configuración de la ventana
        self.geometry("1080x800")
        self.minsize(1080, 800)
        self.maxsize(1080, 800)

        # Configurar fondo con imagen
        background_image = ctk.CTkImage(
            Image.open("recursos/foto_fondo.jpg"),
            size=(1080, 800)
        )
        bg_label = ctk.CTkLabel(self, image=background_image, text="")
        bg_label.place(relwidth=1, relheight=1)

        # Crear widgets estilizados
        self.crear_widgets()

    def crear_widgets(self):
        # Frame principal transparente
        frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=10)
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Título principal con estilo
        title_label = ctk.CTkLabel(
            frame, text="Registrar Habitación",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="white"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Formulario de entrada
        self._crear_campos(frame)

        # Botón de registro
        boton_registrar = ctk.CTkButton(
            frame, text="Registrar Habitación",
            command=self.registrar_o_modificar_habitacion,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#3a3a3a",
            hover_color="#1e90ff"
        )
        boton_registrar.grid(row=5, column=0, columnspan=2, pady=(30, 40))  # Espacio adicional

        # Título para la tabla
        tabla_label = ctk.CTkLabel(
            frame, text="Listado de habitaciones",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        tabla_label.grid(row=6, column=0, columnspan=2, pady=(20, 10))  # Agregado antes de la tabla

        # Tabla para mostrar habitaciones registradas
        self._crear_tabla(frame)

        # Botón "Volver al menú principal"
        volver_button = ctk.CTkButton(
            frame,
            text="Volver",
            command=self.volver_a_pantalla_principal,
            font=ctk.CTkFont(size=16),
            fg_color="#3a3a3a",
            hover_color="#1e90ff"
        )
        volver_button.grid(row=8, column=0, columnspan=2, pady=(30, 10))

        # Centrar ventana y actualizar tabla
        self.update_idletasks()
        self.after(5, lambda: WindowSizeHelper.centrar_ventana(self))
        self.actualizar_tabla()

    def _crear_campos(self, frame):
        """Crea las etiquetas y campos de entrada del formulario."""
        self.tamanio_fuente = 14
        self.fuente = "Arial"
        self.width = 250

        etiquetas_campos = [
            ("Número de Habitación:", 1),
            ("Tipo de Habitación:", 2),
            ("Estado:", 3),
            ("Precio por Noche:", 4),
        ]

        self.entry_numero = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.combo_tipo = ctk.CTkComboBox(frame, values=["Simple", "Doble", "Suite"], width=self.width)
        self.combo_estado = ctk.CTkComboBox(frame, values=["Disponible", "Ocupada"], width=self.width)
        self.entry_precio = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamanio_fuente))

        self.combo_tipo.set("Seleccione un tipo")
        self.combo_estado.set("Seleccione un estado")

        widgets = [self.entry_numero, self.combo_tipo, self.combo_estado, self.entry_precio]

        for texto, fila in etiquetas_campos:
            ctk.CTkLabel(
                frame, text=texto,
                font=(self.fuente, self.tamanio_fuente),
                text_color="white"
            ).grid(row=fila, column=0, padx=10, pady=10, sticky="e")
            widgets[fila - 1].grid(row=fila, column=1, padx=10, pady=10)

    def _crear_tabla(self, frame):
        """Crea la tabla para mostrar habitaciones."""
        self.tabla_habitaciones = ttk.Treeview(
            frame, columns=("numero", "tipo", "estado", "precio"), show="headings"
        )
        self.tabla_habitaciones.heading("numero", text="Número")
        self.tabla_habitaciones.heading("tipo", text="Tipo")
        self.tabla_habitaciones.heading("estado", text="Estado")
        self.tabla_habitaciones.heading("precio", text="Precio por Noche")

        self.tabla_habitaciones.column("numero", width=200)
        self.tabla_habitaciones.column("tipo", width=250)
        self.tabla_habitaciones.column("estado", width=250)
        self.tabla_habitaciones.column("precio", width=250)

        self.tabla_habitaciones.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    # Métodos originales para lógica de negocio
    def registrar_o_modificar_habitacion(self):
        """Lógica para registrar o modificar habitaciones."""
        numero = self.entry_numero.get()
        tipo = self.combo_tipo.get()
        estado = self.combo_estado.get()
        precio = self.entry_precio.get()

        if not numero:
            messagebox.showerror("Error", "Debe seleccionar el número de habitación")
            return

        try:
            habitacion_existente = self.habitacion_service.get_by_id(numero)
            if habitacion_existente:
                self.modificar_habitacion(numero, tipo, estado, precio)
            else:
                self.registrar_habitacion(numero, tipo, estado, precio)
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror('Error', f'No se pudo registrar la habitación: {e}')

    def registrar_habitacion(self, numero, tipo, estado, precio):
        if tipo == "Seleccione un tipo" or estado == "Seleccione un estado" or not precio:
            messagebox.showerror("Error", "Debe completar todos los campos")
            return

        self.habitacion_service.create({"numero": numero, "tipo": tipo, "estado": estado, "precio": precio})
        messagebox.showinfo("Registro exitoso", "Habitación registrada correctamente")
        self.actualizar_tabla()

    def modificar_habitacion(self, numero, tipo, estado, precio):
        if tipo == "Seleccione un tipo":
            tipo = None
        if estado == "Seleccione un estado":
            estado = None

        self.habitacion_service.update(numero, {"numero": numero, "tipo": tipo, "estado": estado, "precio": precio})
        messagebox.showinfo("Modificación exitosa", "Habitación modificada correctamente")
        self.actualizar_tabla()

    def actualizar_tabla(self):
        for row in self.tabla_habitaciones.get_children():
            self.tabla_habitaciones.delete(row)
        for habitacion in self.habitacion_service.get_all():
            self.tabla_habitaciones.insert("", "end", values=(habitacion.numero, habitacion.tipo, habitacion.estado, habitacion.precio_por_noche))

    def limpiar_campos(self):
        self.entry_numero.delete(0, "end")
        self.entry_precio.delete(0, "end")
        self.combo_tipo.set("Seleccione un tipo")
        self.combo_estado.set("Seleccione un estado")

    def volver_a_pantalla_principal(self):
        """Cierra la ventana actual y regresa a la pantalla principal."""
        self.destroy()  # Cierra esta ventana

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from PIL import Image
from clases.cliente import Cliente
from services.cliente_service import ClienteService


class RegistrarCliente(ctk.CTkToplevel):
    def __init__(self, db, pantalla_principal):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.db = db
        self.pantalla_principal = pantalla_principal
        self.cliente_service = ClienteService(db)
        self.title('Registrar Cliente')

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
        frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Título
        ctk.CTkLabel(
            frame, text="Registrar Cliente", font=("Arial", 22, "bold"), text_color="white"
        ).pack(pady=(10, 20))

        # Formulario centrado
        formulario_frame = ctk.CTkFrame(frame, fg_color="transparent")
        formulario_frame.pack(pady=(0, 20), padx=20, expand=True)

        # Campos de entrada
        self.campos = {}
        labels = ["Nro. Documento", "Nombre", "Apellido", "Dirección", "Teléfono", "Email"]
        for i, label_text in enumerate(labels):
            row_frame = ctk.CTkFrame(formulario_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=5, anchor="center")

            ctk.CTkLabel(row_frame, text=label_text, font=("Arial", 14), text_color="white", width=140).pack(side="left")
            self.campos[label_text] = ctk.CTkEntry(row_frame, font=("Arial", 14), width=250)
            self.campos[label_text].pack(side="left", padx=10)

        # Botón para guardar cliente
        boton_guardar = ctk.CTkButton(
            frame, text="Guardar Cliente", command=self.guardar_cliente,
            font=("Arial", 14), fg_color="gray", text_color="white", hover_color="#A9A9A9"
        )
        boton_guardar.pack(pady=(10, 20))

        # Título de la tabla
        ctk.CTkLabel(
            frame, text="Listado de clientes", font=("Arial", 16, "bold"), text_color="white"
        ).pack(pady=(10, 10))

        # Tabla para mostrar clientes registrados
        self.tabla_clientes = ttk.Treeview(
            frame,
            columns=("id_cliente", "nombre", "apellido", "direccion", "telefono", "email", "nro_documento"),
            show="headings"
        )
        self.tabla_clientes.heading("id_cliente", text="ID Cliente")
        self.tabla_clientes.heading("nombre", text="Nombre")
        self.tabla_clientes.heading("apellido", text="Apellido")
        self.tabla_clientes.heading("direccion", text="Dirección")
        self.tabla_clientes.heading("telefono", text="Teléfono")
        self.tabla_clientes.heading("email", text="Email")
        self.tabla_clientes.heading("nro_documento", text="Nro. Documento")
        self.tabla_clientes.pack(pady=10, fill="x", expand=True)

        # Ajustar tamaño de columnas
        for col in self.tabla_clientes["columns"]:
            self.tabla_clientes.column(col, width=120)

        self.actualizar_tabla()

        # Botón de "Volver"
        boton_volver = ctk.CTkButton(
            frame, text="Volver", command=self.volver_a_pantalla_principal,
            font=("Arial", 14), fg_color="gray", text_color="white", hover_color="#A9A9A9"
        )
        boton_volver.pack(pady=(10, 30))

    def guardar_cliente(self):
        """Guarda un cliente en la base de datos."""
        datos = {campo: entrada.get() for campo, entrada in self.campos.items()}
        if not all(datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        cliente = Cliente(**datos)
        self.cliente_service.save(cliente)
        messagebox.showinfo("Éxito", "Cliente registrado exitosamente")
        self.actualizar_tabla()

    def actualizar_tabla(self):
        """Actualiza los datos mostrados en la tabla."""
        for row in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(row)
        for cliente in self.cliente_service.get_all():
            self.tabla_clientes.insert("", "end", values=(
                cliente.id_cliente, cliente.nombre, cliente.apellido,
                cliente.direccion, cliente.telefono, cliente.email, cliente.nro_documento
            ))

    def volver_a_pantalla_principal(self):
        """Cierra la pantalla actual y regresa a la principal."""
        self.destroy()

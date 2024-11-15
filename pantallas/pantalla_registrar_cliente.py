import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from tkinter import messagebox
from pantallas.helpers.window_size_helper import WindowSizeHelper
from clases.cliente import Cliente


from services.cliente_service import ClienteService

class RegistrarCliente(ctk.CTkToplevel):
    def __init__(self, db):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.db = db
        self.cliente_service = ClienteService(db)
        self.title('Registrar Cliente')
        self.clientes = []

        # Tamaño y configuración de la ventana
        self.geometry("1100x800")  # Ajustar el tamaño
        self.minsize(1100, 800)

        self.tamaño_fuente = 14
        self.fuente = "Arial"
        self.width = 250

        # Crear widgets con estilo y valores por defecto
        self.crear_widgets()

    def crear_widgets(self):
        # Frame principal con padding adicional para una apariencia más espaciosa
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Titulo
        ctk.CTkLabel(frame, text='Registrar Cliente', font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=20)

        # Etiquetas y campos de entrada
        ctk.CTkLabel(frame, text="Nombre:",
                     font=(self.fuente, self.tamaño_fuente)
                     ).grid(row=1, column=0, padx=10, pady=10)
        self.entry_nombre = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamaño_fuente))
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame, text="Apellido:",
                     font=(self.fuente, self.tamaño_fuente)
                     ).grid(row=2, column=0, padx=10, pady=10)
        self.entry_apellido = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamaño_fuente))
        self.entry_apellido.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame, text="Dirección:",
                     font=(self.fuente, self.tamaño_fuente)
                     ).grid(row=3, column=0, padx=10, pady=10)
        self.entry_direccion = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamaño_fuente))
        self.entry_direccion.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame, text="Teléfono:",
                     font=(self.fuente, self.tamaño_fuente)
                     ).grid(row=4, column=0, padx=10, pady=10)
        self.entry_telefono = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamaño_fuente))
        self.entry_telefono.grid(row=4, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame, text="Email:",
                     font=(self.fuente, self.tamaño_fuente)
                     ).grid(row=5, column=0, padx=10, pady=10)
        self.entry_email = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamaño_fuente))
        self.entry_email.grid(row=5, column=1, padx=10, pady=10)

        # Tabla para mostrar los clientes registrados
        self.tabla_clientes = ttk.Treeview(frame, columns=("id_cliente", "nombre", "apellido", "direccion", "telefono", "email"), show="headings")
        self.tabla_clientes.heading("id_cliente", text="ID Cliente")
        self.tabla_clientes.heading("nombre", text="Nombre")
        self.tabla_clientes.heading("apellido", text="Apellido")
        self.tabla_clientes.heading("direccion", text="Dirección")
        self.tabla_clientes.heading("telefono", text="Teléfono")
        self.tabla_clientes.heading("email", text="Email")
        self.tabla_clientes.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        # Asignar tamaño a las columnas
        self.tabla_clientes.column("id_cliente", width=100)
        self.tabla_clientes.column("nombre", width=200)
        self.tabla_clientes.column("apellido", width=200)
        self.tabla_clientes.column("direccion", width=150)
        self.tabla_clientes.column("telefono", width=150)
        self.tabla_clientes.column("email", width=200)

        # Botón de registro centrado
        self.registrar_btn = ctk.CTkButton(frame, text='Registrar Cliente', command=self.registrar_cliente,
                                      font=("Arial", 14), width=200, height=40)
        self.registrar_btn.grid(row=6, column=0, columnspan=2, pady=30)

        self.actualizar_tabla()

        # Centrar ventana después de ajustarse al contenido
        self.update_idletasks()
        self.after(5, lambda: WindowSizeHelper.centrar_ventana(self))

    def registrar_cliente(self):

        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        direccion = self.entry_direccion.get()
        telefono = self.entry_telefono.get()
        email = self.entry_email.get()

        # Validaciones Simples
        if not nombre:
            messagebox.showerror("Error", "Debe completar el campo de nombre")
            return
        if not apellido:
            messagebox.showerror("Error", "Debe completar el campo de apellido")
            return
        if not direccion:
            messagebox.showerror("Error", "Debe completar el campo de dirección")
            return
        if not telefono:
            messagebox.showerror("Error", "Debe completar el campo de teléfono")
            return
        if not email:
            messagebox.showerror("Error", "Debe completar el campo de email")
            return

        cliente_data = {
            'nombre': nombre,
            'apellido': apellido,
            'direccion': direccion,
            'telefono': telefono,
            'email': email
        }

        try:
            # Logica de registro
            self.cliente_service.create(cliente_data)
            messagebox.showinfo('Registro exitoso', 'El cliente se ha registrado correctamente.')
            self.limpiar_campos()

            print("Cliente registrado!")
        except Exception as e:
            messagebox.showerror('Error', f'No se pudo registrar el cliente: {e}')


    def limpiar_campos(self):
        self.entry_nombre.delete(0, "end")
        self.entry_apellido.delete(0, "end")
        self.entry_direccion.delete(0, "end")
        self.entry_telefono.delete(0, "end")
        self.entry_email.delete(0, "end")

        self.actualizar_tabla()

    def actualizar_tabla(self):
        for row in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(row)
        for cliente in self.cliente_service.get_all():
            self.tabla_clientes.insert("", "end", values=(cliente.id_cliente, cliente.nombre,
                                                          cliente.apellido, cliente.direccion, cliente.telefono,
                                                          cliente.email))

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from PIL import Image
from clases.cliente import Cliente
from services.cliente_service import ClienteService
import re


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

        # Configurar validaciones
        vcmd_dni = self.register(self.validar_num_rango)
        vcmd_telefono = self.register(self.validar_num_rango)
        vcmd_direccion = self.register(self.validar_direccion)
        vcmd_email = self.register(self.validar_email)
        vcmd_texto = self.register(self.validar_texto)

        # Campos de entrada
        self.campos = {}
        labels = ["Nro. Documento", "Nombre", "Apellido", "Dirección", "Teléfono", "Email"]
        limites = {"Nro. Documento": 8, "Nombre": 50, "Apellido": 50, "Dirección": 100, "Teléfono": 15, "Email": 100}
        for label_text in labels:
            row_frame = ctk.CTkFrame(formulario_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=5, anchor="center")

            ctk.CTkLabel(row_frame, text=label_text, font=("Arial", 14), text_color="white", width=140).pack(
                side="left")

            # Validación por campo
            if label_text == "Nro. Documento":
                self.campos[label_text] = ctk.CTkEntry(
                    row_frame, font=("Arial", 14), width=250,
                    validate="key", validatecommand=(vcmd_dni, "%P", 8)
                )

            elif label_text == "Teléfono":
                self.campos[label_text] = ctk.CTkEntry(
                    row_frame, font=("Arial", 14), width=250,
                    validate="key", validatecommand=(vcmd_telefono, "%P", 15)
                )

            elif label_text == "Dirección":
                self.campos[label_text] = ctk.CTkEntry(
                    row_frame, font=("Arial", 14), width=250,
                    validate="key", validatecommand=(vcmd_direccion, "%P", 100)
                )

            elif label_text == "Email":
                self.campos[label_text] = ctk.CTkEntry(
                    row_frame, font=("Arial", 14), width=250,
                    validate="key", validatecommand=(vcmd_email, "%P", 150)
                )

            else:
                self.campos[label_text] = ctk.CTkEntry(
                    row_frame, font=("Arial", 14), width=250,
                    validate="key", validatecommand=(vcmd_texto, "%P", limites[label_text])
                )
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
            columns=("id_cliente", "nombre", "apellido", "direccion", "telefono", "email", "nro_documento", "puntos"),
            show="headings"
        )
        self.tabla_clientes.heading("id_cliente", text="ID Cliente")
        self.tabla_clientes.heading("nombre", text="Nombre")
        self.tabla_clientes.heading("apellido", text="Apellido")
        self.tabla_clientes.heading("direccion", text="Dirección")
        self.tabla_clientes.heading("telefono", text="Teléfono")
        self.tabla_clientes.heading("email", text="Email")
        self.tabla_clientes.heading("nro_documento", text="Nro. Documento")
        self.tabla_clientes.heading("puntos", text="Puntos")
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

    def validar_num_rango(self, valor, limite):
        """Valida que el dato ingresado sea numérico y no exceda el límite de caracteres."""
        # Permitimos vacío para cuando el campo está vacío (no es obligatorio ingresar el valor de inmediato)
        if valor == "":
            return True

        # Validamos que el valor sea numérico o que contenga un solo punto decimal
        if valor.isdigit() and len(valor) <= int(limite):
            # Se permite un solo punto decimal
            return True

        return False

    def validar_direccion(self, valor, limite):
        """Valida que la dirección permita texto, números, y caracteres comunes, respetando el límite."""
        if valor == "":  # Permitir campo vacío
            return True
        return all(c.isalnum() or c in " ,.-" for c in valor) and len(valor) <= int(limite)

    def validar_email(self, valor, limite):
        """Valida que el email tenga un formato correcto, permita caracteres alfanuméricos, y respete el límite."""
        if valor == "":  # Permitir campo vacío
            return True
        # Regex para validar un email básico
        patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(patron, valor) and len(valor) <= int(limite)

    def validar_texto(self, valor, limite):
        """Valida que el texto solo contenga letras, espacios, y caracteres acentuados, respetando el límite."""
        if valor == "":  # Permitir campo vacío
            return True
        return all(c.isalpha() or c.isspace() for c in valor) and len(valor) <= int(limite)

    def guardar_cliente(self):
        """Guarda un cliente en la base de datos."""
        datos = {
            "nro_documento": self.campos["Nro. Documento"].get(),
            "nombre": self.campos["Nombre"].get(),
            "apellido": self.campos["Apellido"].get(),
            "direccion": self.campos["Dirección"].get(),
            "telefono": self.campos["Teléfono"].get(),
            "email": self.campos["Email"].get()
        }

        # Validar que todos los campos tengan valores
        if not all(datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # Validación de email: verificar que contenga un arroba
        email = datos["email"]
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "El campo Email debe contener un arroba '@' o agregar el dominio.")
            return

        try:
            self.cliente_service.create(datos)  # Pasar el diccionario de datos
            messagebox.showinfo("Éxito", "Cliente registrado exitosamente")
            self.actualizar_tabla()
            self.limpiar_campos()
        except Exception as e:
            print(e)
            messagebox.showerror("Error", f"Hubo un problema al guardar el cliente: {e}")

    def limpiar_campos(self):
        """Limpia los campos del formulario y pone el foco en el primer campo."""
        for campo in self.campos.values():
            campo.delete(0, 'end')  # Elimina el texto dentro del campo

        # Focalizamos el primer campo (Nro. Documento)
        self.campos["Nro. Documento"].focus()

    def actualizar_tabla(self):
        # Limpiar la tabla actual
        for row in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(row)

        # Obtener todos los clientes desde el repositorio
        clientes = self.cliente_service.get_all()

        # Insertar los datos en la tabla
        for cliente in clientes:
            self.tabla_clientes.insert("", "end", values=(cliente.id_cliente, cliente.nombre, cliente.apellido,
                                                          cliente.direccion, cliente.telefono, cliente.email,
                                                          cliente.nro_documento, cliente.puntos_fidelizacion))

    def volver_a_pantalla_principal(self):
        """Cierra la pantalla actual y regresa a la principal."""
        self.destroy()
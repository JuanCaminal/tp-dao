import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from services.habitacion_service import HabitacionService
from pantallas.helpers.window_size_helper import WindowSizeHelper

class RegistrarHabitacion(ctk.CTkToplevel):
    def __init__(self, db):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.db = db
        self.habitacion_service = HabitacionService(db)
        self.title('Registrar Habitación')

        # Tamaño y configuración de la ventana
        self.geometry("1100x800")  # Ajustar el tamaño
        self.minsize(1100, 800)

        self.tamanio_fuente = 14
        self.fuente = "Arial"
        self.width = 250

        # Crear widgets con estilo y valores por defecto
        self.crear_widgets()




    def crear_widgets(self):
        # Frame principal con padding adicional para una apariencia más espaciosa
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Titulo
        ctk.CTkLabel(frame, text='Registrar Habitación', font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=20)

        # Etiquetas y campos de entrada
        ctk.CTkLabel(frame, text="Número de Habitación:",
                     font=(self.fuente, self.tamanio_fuente)
                     ).grid(row=1, column=0, padx=10, pady=10)
        self.entry_numero = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.entry_numero.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame, text="Tipo de Habitación:",
                     font=(self.fuente, self.tamanio_fuente)
                     ).grid(row=2, column=0, padx=10, pady=10)
        self.combo_tipo = ctk.CTkComboBox(frame, values=["Simple", "Doble", "Suite"]
                                          , width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.combo_tipo.grid(row=2, column=1, padx=10, pady=10)
        self.combo_tipo.set("Seleccione un tipo")

        ctk.CTkLabel(frame, text="Estado:",
                     font=(self.fuente, self.tamanio_fuente)
                     ).grid(row=3, column=0, padx=10, pady=10)
        self.combo_estado = ctk.CTkComboBox(frame, values=["Disponible", "Ocupada"],
                                            width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.combo_estado.grid(row=3, column=1, padx=10, pady=10)
        self.combo_estado.set("Seleccione un estado")

        ctk.CTkLabel(frame, text="Precio por Noche:",
                     font=(self.fuente, self.tamanio_fuente)
                     ).grid(row=4, column=0, padx=10, pady=10)
        self.entry_precio = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.entry_precio.grid(row=4, column=1, padx=10, pady=10)

        # Tabla para mostrar las habitaciones registradas
        self.tabla_habitaciones = ttk.Treeview(frame, columns=("numero", "tipo", "estado", "precio"), show="headings")
        self.tabla_habitaciones.heading("numero", text="Número")
        self.tabla_habitaciones.heading("tipo", text="Tipo")
        self.tabla_habitaciones.heading("estado", text="Estado")
        self.tabla_habitaciones.heading("precio", text="Precio por Noche")
        self.tabla_habitaciones.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # asignar tamaño a cada columna
        self.tabla_habitaciones.column("numero", width=200)
        self.tabla_habitaciones.column("tipo", width=250)
        self.tabla_habitaciones.column("estado", width=250)
        self.tabla_habitaciones.column("precio", width=250)

        # Botón para registrar la habitación
        ctk.CTkButton(frame, text="Registrar Habitación", command=self.registrar_o_modificar_habitacion,
                      font=(self.fuente, self.tamanio_fuente)
                      ).grid(row=5, column=0, columnspan=2, pady=10)

        # Centrar ventana después de ajustarse al contenido
        self.update_idletasks()
        self.after(5, lambda: WindowSizeHelper.centrar_ventana(self))

        # Actualizar la tabla
        self.actualizar_tabla()


    def registrar_o_modificar_habitacion(self):
        numero = self.entry_numero.get()
        tipo = self.combo_tipo.get()
        estado = self.combo_estado.get()
        # estado = "Disponible"
        precio = self.entry_precio.get()

        if not numero:
            messagebox.showerror("Error", "Debe seleccionar el numero de habitacion")
            return

        try:
            habitacion_existente = None
            habitacion_existente = self.habitacion_service.get_by_id(numero)
            print("1222")

            if habitacion_existente != None:
                print("holaaaa")
                self.modificar_habitacion(numero, tipo, estado, precio)

            else:
                self.registrar_habitacion(numero, tipo, estado, precio)
            self.limpiar_campos()

        except Exception as e:
            messagebox.showerror('Error', f'No se pudo registrar la habitación: {e}')


    def registrar_habitacion(self, numero, tipo, estado, precio):
        if tipo == "Seleccione un tipo" or estado == "Seleccione un estado":
            messagebox.showerror("Error", "Debe seleccionar un tipo y un estado")
            return

        if not precio:
            messagebox.showerror("Error", "Debe ponerle un precio a una nueva habitacion")
            return

        habitacion_data = {
            "numero": numero,
            "tipo": tipo,
            "estado": estado,
            "precio": precio
        }

        self.habitacion_service.create(habitacion_data)
        messagebox.showinfo("Registro exitoso", "Habitación registrada correctamente")

    def modificar_habitacion(self, numero, tipo, estado, precio):

        if tipo == "Seleccione un tipo" and estado == "Seleccione un estado":
            messagebox.showerror("Error", "Debe seleccionar un tipo o un estado, para modificar una habitacion")
            return

        if tipo == "Seleccione un tipo":
            tipo = None
        if estado == "Seleccione un estado":
            estado = None


        habitacion_data = {
            "numero": numero,
            "tipo": tipo,
            "estado": estado,
            "precio": precio
        }

        self.habitacion_service.update(numero, habitacion_data)
        messagebox.showinfo("Modificacion exitosa", "Habitación modificada correctamente")


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
        self.actualizar_tabla()


from tkinter import *
from tkcalendar import Calendar
from datetime import datetime
from pantallas.helpers.window_size_helper import WindowSizeHelper
import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from pantallas import pantalla_principal
from services.habitacion_service import HabitacionService
from services.cliente_service import ClienteService
from services.reserva_service import ReservaService


class RegistrarReserva(ctk.CTkToplevel):
    def __init__(self, db, pantalla_principal):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.db = db
        self.title('Registrar Reserva')

        # Tamaño y configuración de la ventana
        self.geometry("1100x800")
        self.minsize(1100, 800)
        self.maxsize(1100, 800)

        self.tamanio_fuente = 14
        self.fuente = "Arial"
        self.width = 250

        self.habitacion_service = HabitacionService(db)
        self.cliente_service = ClienteService(db)
        self.reserva_service = ReservaService(db)

        self.clientes = self.cliente_service.get_all()
        self.habitaciones = self.habitacion_service.get_all()
        self.reservas = self.reserva_service.get_all()

        # Crear widgets con estilo y valores por defecto
        self.crear_widgets()

    def crear_widgets(self):
        # Imagen de fondo
        canvas = Canvas(self, width=1100, height=800)
        canvas.pack(fill="both", expand=True)

        # Cargar y mostrar la imagen de fondo
        self.bg_image = ImageTk.PhotoImage(Image.open("recursos/foto_fondo.jpg"))
        canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Frame principal encima del fondo
        frame = ctk.CTkFrame(self, corner_radius=10, bg_color="transparent")
        canvas.create_window(550, 300, window=frame, width=1000, height=550, anchor="center")

        # Título
        ctk.CTkLabel(frame, text='Registrar Reserva', font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=20)

        # Etiquetas y campos de entrada

        ctk.CTkLabel(frame, text="Cliente:",
                     font=(self.fuente, self.tamanio_fuente)
                     ).grid(row=1, column=0, padx=10, pady=10)
        self.combo_cliente = ctk.CTkComboBox(frame, values=[f"{cliente.nombre} {cliente.apellido}" for cliente in
                                                            self.clientes]
                                             , width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.combo_cliente.grid(row=1, column=1, padx=10, pady=10)
        self.combo_cliente.set("Seleccione un cliente")

        ctk.CTkLabel(frame, text="Habitación:",
                     font=(self.fuente, self.tamanio_fuente,)
                     ).grid(row=2, column=0, padx=10, pady=10)
        self.combo_habitacion = ctk.CTkComboBox(frame,
                                                values=[f"{habitacion.numero} - {habitacion.tipo}" for habitacion in
                                                        self.habitaciones]
                                                , width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.combo_habitacion.grid(row=2, column=1, padx=10, pady=10)
        self.combo_habitacion.set("Seleccione una habitación")

        ctk.CTkLabel(frame, text="Fecha de Entrada (dd/mm/YYYY):",
                     font=(self.fuente, self.tamanio_fuente)
                     ).grid(row=3, column=0, rowspan=2, padx=10, pady=10)
        self.entry_fecha_entrada = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.entry_fecha_entrada.insert(0, self.fecha_actual())
        self.entry_fecha_entrada.grid(row=3, column=1, padx=10, pady=10)
        self.open_calendar_fecha_entrada = ctk.CTkButton(frame, text="Seleccionar Fecha",
                                                         command=lambda: self.open_calendar("fecha_entrada"))
        self.open_calendar_fecha_entrada.grid(row=4, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame, text="Fecha de Salida (dd/mm/YYYY):",
                     font=(self.fuente, self.tamanio_fuente)).grid(row=5, column=0, rowspan=2, padx=10, pady=10)
        self.entry_fecha_salida = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.entry_fecha_salida.grid(row=5, column=1, padx=10, pady=10)

        self.open_calendar_fecha_salida = ctk.CTkButton(frame, text="Seleccionar Fecha",
                                                        command=lambda: self.open_calendar("fecha_salida"))
        self.open_calendar_fecha_salida.grid(row=6, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame, text="Cantidad de Personas:",
                     font=(self.fuente, self.tamanio_fuente)
                     ).grid(row=7, column=0, padx=10, pady=10)
        self.entry_cantidad_personas = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.entry_cantidad_personas.grid(row=7, column=1, padx=10, pady=10)

        # Botón para registrar reserva
        ctk.CTkButton(frame, text="Registrar Reserva", command=self.registrar_reserva).grid(row=8, column=0,
                                                                                            columnspan=2, pady=10)

        # Tabla para mostrar las reservas registradas
        self.tabla_reservas = ttk.Treeview(frame, columns=(
            "id_reserva", "cliente", "habitacion", "fecha_entrada", "fecha_salida", "cantidad_personas"),
                                           show="headings")

        self.tabla_reservas.heading("id_reserva", text="ID Reserva")
        self.tabla_reservas.heading("cliente", text="Cliente")
        self.tabla_reservas.heading("habitacion", text="Habitación")
        self.tabla_reservas.heading("fecha_entrada", text="Fecha de Entrada")
        self.tabla_reservas.heading("fecha_salida", text="Fecha de Salida")
        self.tabla_reservas.heading("cantidad_personas", text="Personas")

        self.tabla_reservas.column("id_reserva", width=80, anchor="center")
        self.tabla_reservas.column("cliente", width=200, anchor="center")
        self.tabla_reservas.column("habitacion", width=200, anchor="center")
        self.tabla_reservas.column("fecha_entrada", width=140, anchor="center")
        self.tabla_reservas.column("fecha_salida", width=140, anchor="center")
        self.tabla_reservas.column("cantidad_personas", width=100, anchor="center")

        self.tabla_reservas.grid(row=9, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        # Configurar el frame para centrado
        frame.grid_rowconfigure(9, weight=1)  # Permite que la fila con la tabla tome espacio disponible
        frame.grid_columnconfigure(0, weight=1)  # Centra la tabla en el frame

        # Botón "Volver" centrado debajo de la tabla
        boton_volver = ctk.CTkButton(
            self, text="Volver", command=self.volver_a_pantalla_principal,
            font=("Arial", 14), fg_color="gray", text_color="white", hover_color="#A9A9A9"
        )
        canvas.create_window(550, 730, window=boton_volver, anchor="center")

        self.update_idletasks()
        self.after(5, lambda: WindowSizeHelper.centrar_ventana(self))

        self.actualizar_tabla()

        # Botón "Volver" centrado debajo de la tabla
        boton_volver = ctk.CTkButton(
            self, text="Volver", command=self.volver_a_pantalla_principal,
            font=("Arial", 14), fg_color="gray", text_color="white", hover_color="#A9A9A9"
        )
        canvas.create_window(550, 730, window=boton_volver, anchor="center")

        self.update_idletasks()
        self.after(5, lambda: WindowSizeHelper.centrar_ventana(self))

    def ir_pantalla_principal(self):
        self.destroy()
        pantalla_principal.PantallaPrincipal(self.db)

    def open_calendar(self, tipo_fecha):
        top = Toplevel(self)
        top.grab_set()

        top.title("Seleccionar Fecha")
        cal = Calendar(top, selectmode='day', date_pattern='dd/mm/yyyy')
        cal.pack(pady=20)

        select_button = ttk.Button(top, text="Confirmar", command=lambda: self.select_date(cal, top, tipo_fecha))
        select_button.pack(pady=10)

        top.update_idletasks()
        WindowSizeHelper.centrar_ventana(top)

    def select_date(self, cal, top, tipo_fecha):
        if tipo_fecha == "fecha_entrada":
            self.entry_fecha_entrada.delete(0, "end")
            self.entry_fecha_entrada.insert(0, cal.get_date())
        else:
            self.entry_fecha_salida.delete(0, "end")
            self.entry_fecha_salida.insert(0, cal.get_date())
        top.destroy()

    def fecha_actual(self):
        return datetime.now().strftime("%d/%m/%Y")

    def registrar_reserva(self):
        cliente_nombre = self.combo_cliente.get()
        habitacion_nro_tipo = self.combo_habitacion.get()
        fecha_entrada = self.entry_fecha_entrada.get()
        fecha_salida = self.entry_fecha_salida.get()
        cantidad_personas = self.entry_cantidad_personas.get()

        if cliente_nombre == "Seleccione un cliente" or habitacion_nro_tipo == "Seleccione una habitación" or fecha_entrada == "" or fecha_salida == "" or cantidad_personas == "":
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return

        # Obtener el id del cliente y la habitación
        for cliente in self.clientes:
            if cliente.nombre + " " + cliente.apellido == cliente_nombre:
                cliente_id = cliente.id_cliente
                break

        habitacion_nro = int(habitacion_nro_tipo.split(" - ")[0])
        habitacion_tipo = habitacion_nro_tipo.split(" - ")[1]

        fecha_entrada = datetime.strptime(fecha_entrada, "%d/%m/%Y").strftime("%Y-%m-%d")
        fecha_salida = datetime.strptime(fecha_salida, "%d/%m/%Y").strftime("%Y-%m-%d")

        # Validar fechas y validar que la cantidad de personas no exceda la que permite la habitacion
        if fecha_entrada > fecha_salida:
            messagebox.showerror("Error", "Por favor ingrese una fecha válida")
            return

        if fecha_entrada < self.fecha_actual():
            messagebox.showerror("Error", "Por favor ingrese una fecha posterior a la fecha actual")
            return

        # Obtener el tipo de habitacion
        match habitacion_tipo.lower():
            case "simple":
                if int(cantidad_personas) > 1:
                    messagebox.showerror("Error", "Por favor ingrese una cantidad de personas valida")
                    return
            case "doble":
                if int(cantidad_personas) > 2:
                    messagebox.showerror("Error", "Por favor ingrese una cantidad de personas valida")
                    return
            case "suite":
                if int(cantidad_personas) > 4:
                    messagebox.showerror("Error", "Por favor ingrese una cantidad de personas valida")
                    return
            case _:
                print("Tipo de habitación no valida")
                messagebox.showerror("Error", "Lo sentimos ocurrio un error de base de datos")
                return

        if not self.verificar_disponibilidad_habitacion(habitacion_nro, fecha_entrada, fecha_salida):
            messagebox.showinfo("Habitacion ocupada",
                                "La habitacion no esta disponible en la fecha solicitada. \n Por favor, seleccione otra habitacion o seleccione una fecha distinta. ")
            return

        reserva_data = {
            "cliente": cliente_id,
            "habitacion": habitacion_nro,
            "fecha_entrada": fecha_entrada,
            "fecha_salida": fecha_salida,
            "cantidad_personas": cantidad_personas
        }

        try:
            self.reserva_service.create(reserva_data)
            messagebox.showinfo("Registro exitoso", "Reserva registrada correctamente")
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror('Error', f'No se pudo registrar la reserva: {e}')

    def limpiar_campos(self):
        self.combo_cliente.set("Seleccione un cliente")
        self.combo_habitacion.set("Seleccione una habitación")
        self.entry_fecha_entrada.delete(0, "end")
        nueva_fecha = self.fecha_actual()
        self.entry_fecha_entrada.insert(0, nueva_fecha)
        self.entry_fecha_salida.delete(0, "end")
        self.entry_cantidad_personas.delete(0, "end")
        self.actualizar_tabla()

    def actualizar_tabla(self):
        for row in self.tabla_reservas.get_children():
            self.tabla_reservas.delete(row)
        for reserva in self.reserva_service.get_all():
            cliente = self.cliente_service.get_by_id(reserva.cliente)
            habitacion = self.habitacion_service.get_by_id(reserva.habitacion)
            self.tabla_reservas.insert("", "end", values=(reserva.id_reserva, f"{cliente.nombre} {cliente.apellido}",
                                                          f"{habitacion.numero} - {habitacion.tipo}",
                                                          reserva.fecha_entrada, reserva.fecha_salida,
                                                          reserva.cantidad_personas))

    def verificar_disponibilidad_habitacion(self, habitacion_nro, fecha_entrada, fecha_salida):

        for reserva in self.reservas:
            if reserva.habitacion == habitacion_nro and (
                    reserva.fecha_entrada <= fecha_entrada <= reserva.fecha_salida or reserva.fecha_entrada <= fecha_salida <= reserva.fecha_salida):
                return False

        return True

    def volver_a_pantalla_principal(self):
        """Cierra la pantalla actual y regresa a la principal."""
        self.destroy()

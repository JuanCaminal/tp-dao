import customtkinter as ctk
from tkinter import ttk, messagebox, Toplevel
from tkcalendar import Calendar
from services.empleado_service import EmpleadoService
from services.habitacion_service import HabitacionService
from pantallas.helpers.window_size_helper import WindowSizeHelper
from datetime import datetime
from PIL import Image
from customtkinter import CTkImage

class AsignarEmpleadoXHabitacion(ctk.CTkToplevel):
    def __init__(self, db):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.db = db
        self.habitacion_service = HabitacionService(db)
        self.empleado_service = EmpleadoService(db)
        self.title('Registrar Empleado por Habitación')

        # Levanta la ventana y la pone en primer plano
        self.lift()
        self.attributes('-topmost', True)  # Mantener siempre en primer plano
        self.after(100, lambda: self.attributes('-topmost', False))  # Una vez mostrada, quitar topmost para evitar problemas al cambiar de ventana.

        # Tamaño y configuración de la ventana
        WindowSizeHelper.set_size(self, 1150, 800)
        self.minsize(1150, 800)
        self.maxsize(1150, 800)

        self.tamanio_fuente = 14
        self.fuente = "Arial"
        self.width = 250

        self.habitaciones = self.habitacion_service.get_all()
        self.empleados = self.empleado_service.get_all()

        # Cargar imagen de fondo con CTkImage
        self.bg_image = CTkImage(light_image=Image.open("recursos/foto_fondo.jpg"), size=(1150, 800))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(relwidth=1, relheight=1)

        # Crear widgets con estilo y valores por defecto
        self.crear_widgets()

    def crear_widgets(self):
        # Frame principal con padding adicional para una apariencia más espaciosa
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Titulo
        ctk.CTkLabel(frame, text='Registrar Empleado Por Habitacion', font=("Arial", 18)).grid(row=0, column=0,
                                                                                               columnspan=2, pady=20)

        # Combo Empleado
        ctk.CTkLabel(frame, text="Empleado:",
                     font=(self.fuente, self.tamanio_fuente,)
                     ).grid(row=1, column=0, padx=10, pady=10)
        self.combo_empleado = ctk.CTkComboBox(frame,
                                              values=[f"{empleado.apellido}, {empleado.nombre}" for empleado in
                                                      self.empleados]
                                              , width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.combo_empleado.grid(row=1, column=1, padx=10, pady=10)
        self.combo_empleado.set("Seleccione un empleado")

        # Combo Habitacion
        ctk.CTkLabel(frame, text="Habitación:",
                     font=(self.fuente, self.tamanio_fuente,)
                     ).grid(row=2, column=0, padx=10, pady=10)
        self.combo_habitacion = ctk.CTkComboBox(frame,
                                                values=[f"{habitacion.numero} - {habitacion.tipo}" for habitacion in
                                                        self.habitaciones]
                                                , width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.combo_habitacion.grid(row=2, column=1, padx=10, pady=10)
        self.combo_habitacion.set("Seleccione una habitación")

        # Fecha de asignacion
        ctk.CTkLabel(frame, text="Fecha de Asignacion (dd/mm/YYYY):",
                     font=(self.fuente, self.tamanio_fuente)
                     ).grid(row=3, column=0, padx=10, pady=10)

        self.entry_fecha_asignacion = ctk.CTkEntry(frame, width=self.width, font=(self.fuente, self.tamanio_fuente))
        self.entry_fecha_asignacion.insert(0, self.fecha_actual())
        self.entry_fecha_asignacion.grid(row=3, column=1, padx=10, pady=10)
        self.open_calendar_fecha_asignacion = ctk.CTkButton(frame, text="Seleccionar Fecha",
                                                            command=lambda: self.open_calendar("fecha_asignacion"))
        self.open_calendar_fecha_asignacion.grid(row=4, column=1, padx=10, pady=10)

        # Tarea
        ctk.CTkLabel(frame, text="Tarea:",
                     font=(self.fuente, self.tamanio_fuente,)
                     ).grid(row=5, column=0, padx=10, pady=10)
        self.entry_tarea = ctk.CTkEntry(frame, width=self.width * 1.5,
                                        height=80,
                                        font=(self.fuente, self.tamanio_fuente))
        self.entry_tarea.grid(row=5, column=1, padx=10, rowspan=2, pady=10)

        # Botón para asignar empleado
        ctk.CTkButton(frame, text="Asignar Empleado", command=self.asignar_empleado_habitacion).grid(row=7, column=0,
                                                                                                     columnspan=2,
                                                                                                     pady=25)

        self.tabla_asignaciones = ttk.Treeview(frame, columns=(
            "id_asignacion", "empleado", "habitacion", "fecha_asignacion", "tarea"),
                                               show="headings")
        self.tabla_asignaciones.heading("id_asignacion", text="ID Asignacion")
        self.tabla_asignaciones.heading("empleado", text="Empleado")
        self.tabla_asignaciones.heading("habitacion", text="Habitación")
        self.tabla_asignaciones.heading("fecha_asignacion", text="Fecha de Asignacion")
        self.tabla_asignaciones.heading("tarea", text="Tarea")
        self.tabla_asignaciones.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # asignar tamaño a cada columna
        self.tabla_asignaciones.column("id_asignacion", width=100)
        self.tabla_asignaciones.column("empleado", width=250)
        self.tabla_asignaciones.column("habitacion", width=150)
        self.tabla_asignaciones.column("fecha_asignacion", width=150)
        self.tabla_asignaciones.column("tarea", width=450)

        # Botón para volver a la pantalla anterior
        ctk.CTkButton(frame, text="Volver", command=self.destroy,
            font=("Arial", 14), fg_color="gray", text_color="white", hover_color="#A9A9A9"
            ).grid(row=9, column=0, columnspan=2, pady=20)

        self.update_idletasks()
        self.after(5, lambda: WindowSizeHelper.centrar_ventana(self))

        self.actualizar_tabla()

    def asignar_empleado_habitacion(self):
        empleado_apellido_nombre = self.combo_empleado.get()
        habitacion_numero_tipo = self.combo_habitacion.get()
        fecha_asignacion = self.entry_fecha_asignacion.get()
        tarea = self.entry_tarea.get()

        if empleado_apellido_nombre == "Seleccione un empleado" or habitacion_numero_tipo == "Seleccione una habitación" or fecha_asignacion == "Seleccionar Fecha" or tarea == "":
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return

        if fecha_asignacion < self.fecha_actual():
            messagebox.showerror("Error", "Ingrese una fecha válida a la actual")
            return

        empleado_apellido = empleado_apellido_nombre.split(",")[0].strip()
        empleado_nombre = empleado_apellido_nombre.split(",")[1].strip()

        for empleado in self.empleados:
            if empleado.apellido == empleado_apellido and empleado.nombre == empleado_nombre:
                empleado_id = empleado.id_empleado
                break

        habitacion_numero = habitacion_numero_tipo.split(" - ")[0].strip()
        fecha_asignacion = datetime.strptime(fecha_asignacion, "%d/%m/%Y").strftime("%Y-%m-%d")

        asignacion_data = {
            "empleado": empleado_id,
            "habitacion": habitacion_numero,
            "fecha_asignacion": fecha_asignacion,
            "tarea": tarea,
        }

        try:
            self.empleado_service.create_asignacion(asignacion_data)
            messagebox.showinfo("Registro exitoso", "Se asignó el empleado a la habitación correctamente")
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror('Error', f'No se pudo asignar el empleado: {e}')

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

    def fecha_actual(self):
        return datetime.now().strftime("%d/%m/%Y")

    def select_date(self, cal, top, tipo_fecha):
        if tipo_fecha == "fecha_asignacion":
            self.entry_fecha_asignacion.delete(0, "end")
            self.entry_fecha_asignacion.insert(0, cal.get_date())

        top.destroy()

    def actualizar_tabla(self):
        for row in self.tabla_asignaciones.get_children():
            self.tabla_asignaciones.delete(row)

        for asignacion in self.empleado_service.get_all_asignaciones():
            empleado = self.empleado_service.get_by_id(asignacion.empleado_id)
            habitacion = self.habitacion_service.get_by_id(asignacion.habitacion_numero)
            self.tabla_asignaciones.insert("", "end", values=(
                asignacion.id_asignacion,
                f"{empleado.nombre} {empleado.apellido}",
                f"{habitacion.numero} - {habitacion.tipo}",
                asignacion.fecha_asignacion,
                asignacion.tarea
            ))

    def limpiar_campos(self):
        self.combo_empleado.set("Seleccione un empleado")
        self.combo_habitacion.set("Seleccione una habitación")
        self.entry_fecha_asignacion.delete(0, "end")
        nueva_fecha = self.fecha_actual()
        self.entry_fecha_asignacion.insert(0, nueva_fecha)
        self.entry_tarea.delete(0, "end")
        self.actualizar_tabla()



import customtkinter as ctk
from tkinter import messagebox, ttk, Toplevel, StringVar
from tkcalendar import Calendar

from pantallas.helpers.window_size_helper import WindowSizeHelper
from services.reporte_service import ReporteService
from services.reserva_service import ReservaService


import customtkinter as ctk
from tkinter import messagebox, ttk, Toplevel, StringVar
from tkcalendar import Calendar

from pantallas.helpers.window_size_helper import WindowSizeHelper
from services.reporte_service import ReporteService
from reportes.reporte_ocupacion_promedio import generar_reporte_ocupacion_promedio


class PantallaReporteReservas(ctk.CTkToplevel):
    def __init__(self, db, reporte_service):
        super().__init__()

        self.db = db
        self.reporte_service = reporte_service

        self.title("Reporte de Reservas")
        self.geometry("800x400")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Etiqueta de título
        title_label = ctk.CTkLabel(self, text="Generar Reporte de Reservas",
                                   font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=10)

        # Contenedor principal
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Entrada para Fecha de Inicio con botón
        fecha_inicio_label = ctk.CTkLabel(frame, text="Fecha de Entrada:", font=ctk.CTkFont(size=14))
        fecha_inicio_label.pack(anchor="w", pady=5)

        self.fecha_inicio_var = StringVar()
        fecha_inicio_entry = ctk.CTkEntry(frame, textvariable=self.fecha_inicio_var, state="readonly", width=200)
        fecha_inicio_entry.pack(pady=5)

        fecha_inicio_button = ctk.CTkButton(frame, text="Seleccionar Fecha de Inicio",
                                            command=self.mostrar_calendario_inicio)
        fecha_inicio_button.pack(pady=5)

        # Entrada para Fecha de Fin con botón
        fecha_fin_label = ctk.CTkLabel(frame, text="Fecha de Salida:", font=ctk.CTkFont(size=14))
        fecha_fin_label.pack(anchor="w", pady=5)

        self.fecha_fin_var = StringVar()
        fecha_fin_entry = ctk.CTkEntry(frame, textvariable=self.fecha_fin_var, state="readonly", width=200)
        fecha_fin_entry.pack(pady=5)

        fecha_fin_button = ctk.CTkButton(frame, text="Seleccionar Fecha de Fin",
                                         command=self.mostrar_calendario_fin)
        fecha_fin_button.pack(pady=5)

        # Botón para generar el reporte
        generar_button = ctk.CTkButton(frame, text="Generar Reporte", width=200, command=self.generar_reporte)
        generar_button.pack(pady=20)

        # Tabla para mostrar los datos
        self.tabla = ttk.Treeview(self, columns=("id_reserva", "cliente_id", "habitacion_numero",
                                                 "fecha_entrada", "fecha_salida", "cantidad_personas"),
                                  show="headings", height=10)
        self.tabla.heading("id_reserva", text="ID Reserva")
        self.tabla.heading("cliente_id", text="ID Cliente")
        self.tabla.heading("habitacion_numero", text="Habitación")
        self.tabla.heading("fecha_entrada", text="Fecha Entrada")
        self.tabla.heading("fecha_salida", text="Fecha Salida")
        self.tabla.heading("cantidad_personas", text="Personas")
        self.tabla.pack(pady=10, fill="both", expand=True)

    def mostrar_calendario_inicio(self):
        self.mostrar_calendario("inicio")

    def mostrar_calendario_fin(self):
        self.mostrar_calendario("fin")

    def mostrar_calendario(self, tipo):
        top_cal = Toplevel(self)
        top_cal.title("Seleccionar Fecha")

        # Crear calendario
        calendario = Calendar(top_cal, date_pattern="yyyy-mm-dd", selectmode="day")
        calendario.pack(pady=20)

        def seleccionar_fecha():
            fecha_seleccionada = calendario.get_date()
            if tipo == "inicio":
                self.fecha_inicio_var.set(fecha_seleccionada)
            else:
                self.fecha_fin_var.set(fecha_seleccionada)
            top_cal.destroy()

        confirmar_button = ctk.CTkButton(top_cal, text="Seleccionar", command=seleccionar_fecha)
        confirmar_button.pack(pady=10)

    def generar_reporte(self):
        """Genera el reporte de reservas para las fechas seleccionadas."""
        try:
            fecha_inicio = self.fecha_inicio_var.get()
            fecha_fin = self.fecha_fin_var.get()

            # Validaciones de las fechas
            if not fecha_inicio or not fecha_fin:
                messagebox.showerror("Error", "Debe seleccionar ambas fechas.")
                return
            if fecha_inicio > fecha_fin:
                messagebox.showerror("Error", "La fecha de inicio no puede ser posterior a la fecha de fin.")
                return


            # Llamar al servicio para obtener reservas
            reservas = self.reporte_service.obtener_reservas_por_fecha(fecha_inicio, fecha_fin)

            # Limpiar la tabla antes de insertar nuevos datos
            for row in self.tabla.get_children():
                self.tabla.delete(row)

            # Insertar las reservas en la tabla
            if reservas:
                for reserva in reservas:
                    self.tabla.insert("", "end", values=reserva)
            else:
                messagebox.showinfo("Sin datos", "No se encontraron reservas para el rango de fechas seleccionado.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {e}")


class PantallaReportes(ctk.CTkToplevel):
    def __init__(self, db):
        super().__init__()

        self.db = db
        self.reporte_service = ReporteService(db)

        self.title("Reportes")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.resizable(True, True)

        label = ctk.CTkLabel(self, text=" -  Seleccione el reporte que desea generar  - ",
                             font=ctk.CTkFont(size=18, weight="bold"))
        label.pack(pady=(30, 20))

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=30, padx=30)

        botones = [
            ("Listar Reservas", self.abrir_reporte_reservas),
            ("Ingresos por habitaciones", self.generar_reporte_ingresos_por_habitaciones),
            ("Ocupación Promedio", self.generar_reporte_ocupacion_promedio),
        ]

        for texto, comando in botones:
            boton = ctk.CTkButton(button_frame, text=texto, command=comando, width=300, height=40,
                                  font=ctk.CTkFont(size=16))
            boton.pack(pady=10)

        self.update_idletasks()
        self.after(10, lambda: WindowSizeHelper.centrar_ventana(self))

    def abrir_reporte_reservas(self):
        PantallaReporteReservas(self.db, self.reporte_service).grab_set()

    def generar_reporte_ingresos_por_habitaciones(self):
        try:
            self.reporte_service.generar_reporte_ingresos_por_habitaciones()
            messagebox.showinfo("Reporte exitoso", "Reporte de Ingresos por habitaciones generado con éxito")
        except Exception as e:
            messagebox.showerror('Error', f'No se pudo generar el reporte: {e}')

    def generar_reporte_ocupacion_promedio(self):
        try:
            generar_reporte_ocupacion_promedio(self, tipo='Simple', estado='ocupada')
            messagebox.showinfo("Reporte exitoso", "Reporte de ocupación promedio generado con éxito")
        except Exception as e:
            messagebox.showerror('Error', f'No se pudo generar el reporte: {e}')

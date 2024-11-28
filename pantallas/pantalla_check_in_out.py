import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime

from selenium.webdriver.common.devtools.v85.inspector import enable

from repositories.reserva_repository import ReservaRepository
from repositories.habitacion_repository import HabitacionRepository
from repositories.factura_repositoy import FacturaRepository
from clases.factura import Factura
from services.cliente_service import ClienteService


class CheckInOut(ctk.CTkToplevel):
    def __init__(self, db):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.db = db
        self.title("Check-In y Check-Out")
        self.geometry("1100x800")
        self.minsize(1100, 800)

        # Variables para la lógica
        self.opciones_combobox = ["Check-In", "Check-Out"]
        self.estado_actual = tk.StringVar(value=self.opciones_combobox[0])  # Estado inicial: Check-In
        self.dni_filtro = tk.StringVar()
        self.usar_puntos = tk.BooleanVar(value=False)  # Variable para el estado del checkbox

        # Crear widgets de la interfaz
        self.crear_widgets()

    def crear_widgets(self):
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Título
        ctk.CTkLabel(frame, text="Check-In y Check-Out", font=("Arial", 18)).pack(pady=20)

        # Combobox para seleccionar Check-In o Check-Out
        ctk.CTkLabel(frame, text="Seleccione una opción:", font=("Arial", 14)).pack(pady=5)
        self.combobox_estado = ctk.CTkComboBox(frame, values=self.opciones_combobox, variable=self.estado_actual,
                                               font=("Arial", 14))
        self.combobox_estado.pack(pady=5)
        self.combobox_estado.bind("<<ComboboxSelected>>", self.actualizar_tabla)  # Actualizar tabla según selección

        # Campo para filtrar por DNI
        ctk.CTkLabel(frame, text="Filtrar por DNI:", font=("Arial", 14)).pack(pady=10)
        filtro_frame = ctk.CTkFrame(frame, corner_radius=0)
        filtro_frame.pack(pady=5)
        ctk.CTkEntry(filtro_frame, textvariable=self.dni_filtro, width=300, font=("Arial", 14)).pack(side="left",
                                                                                                     padx=5)
        ctk.CTkButton(filtro_frame, text="Buscar", command=self.actualizar_tabla).pack(side="left", padx=5)

        # Tabla para mostrar las reservas
        self.tabla_reservas = ttk.Treeview(frame, columns=("id_reserva", "cliente", "habitacion", "fecha", "estado"),
                                           show="headings")
        self.tabla_reservas.heading("id_reserva", text="ID Reserva")
        self.tabla_reservas.heading("cliente", text="Cliente")
        self.tabla_reservas.heading("habitacion", text="Habitación")
        self.tabla_reservas.heading("fecha", text="Fecha")
        self.tabla_reservas.heading("estado", text="Estado")
        self.tabla_reservas.pack(fill="both", expand=True, pady=20)

        # Ajustar columnas
        self.tabla_reservas.column("id_reserva", width=100)
        self.tabla_reservas.column("cliente", width=250)
        self.tabla_reservas.column("habitacion", width=200)
        self.tabla_reservas.column("fecha", width=150)
        self.tabla_reservas.column("estado", width=150)

        # Checkbox para usar puntos de descuento
        self.checkbox_puntos = ctk.CTkCheckBox(frame, text="Usar puntos de descuento", variable=self.usar_puntos,
                                                font=("Arial", 14))
        self.checkbox_puntos.pack(pady=10)

        # Botón para confirmar la acción
        ctk.CTkButton(frame, text="Confirmar", command=self.confirmar_accion).pack(pady=10)

        # Actualizar tabla inicial
        self.actualizar_tabla()

    def fecha_actual(self):
        return datetime.now().strftime("%d/%m/%Y")

    def actualizar_tabla(self, event=None):
        # Limpiar la tabla
        for row in self.tabla_reservas.get_children():
            self.tabla_reservas.delete(row)

        # Obtener el estado actual (Check-In o Check-Out) y el filtro por DNI
        estado = self.estado_actual.get()
        dni_filtro = self.dni_filtro.get().strip()

        # Instanciar el repositorio de reservas
        reserva_repo = ReservaRepository(self.db)

        # Obtener reservas desde la base de datos (ahora devuelve tuplas de Reserva y estado_habitacion)
        reservas_con_estado = reserva_repo.get_reserva_chek_in_out()

        fecha_actual = self.fecha_actual()

        # Filtrar las reservas según el estado
        if estado == "Check-In":
            reservas_con_estado = [
                (reserva, estado_habitacion) for reserva, estado_habitacion in reservas_con_estado
                if
                reserva.fecha_entrada <= fecha_actual and reserva.fecha_salida >= fecha_actual and estado_habitacion == "Disponible"
            ]
        elif estado == "Check-Out":
            reservas_con_estado = [
                (reserva, estado_habitacion) for reserva, estado_habitacion in reservas_con_estado
                if (reserva.fecha_salida < fecha_actual or reserva.fecha_entrada <= fecha_actual and reserva.fecha_salida >= fecha_actual) and estado_habitacion == "Ocupada"
            ]

        # Filtrar por DNI si se especifica
        if dni_filtro:
            reservas_con_estado = [
                (reserva, estado_habitacion) for reserva, estado_habitacion in reservas_con_estado
                if dni_filtro in reserva.cliente
            ]

        # Insertar datos en la tabla (solo usando el objeto Reserva)
        for reserva, _ in reservas_con_estado:
            self.tabla_reservas.insert("", "end", values=(
                reserva.id_reserva, reserva.cliente, reserva.habitacion,
                reserva.fecha_entrada, reserva.fecha_salida, estado
            ))

    def simular_consulta(self, estado, dni):
        # Esto es un ejemplo simulado, reemplazar con tu lógica real
        reservas_ejemplo = [
            {"id": 1, "cliente": "Juan Pérez", "habitacion": "101", "fecha": "27/11/2024", "estado": "Disponible"},
            {"id": 2, "cliente": "Ana Gómez", "habitacion": "102", "fecha": "27/11/2024", "estado": "Ocupada"},
        ]

        if estado == "Check-In":
            reservas = [r for r in reservas_ejemplo if r["estado"] == "Disponible"]
        else:
            reservas = [r for r in reservas_ejemplo if r["estado"] == "Ocupada"]

        if dni:
            reservas = [r for r in reservas if dni in r["cliente"]]

        return reservas

    def confirmar_accion(self):
        try:
            # Obtener la selección en la tabla
            seleccion = self.tabla_reservas.selection()
            if not seleccion:
                messagebox.showerror("Error", "Debe seleccionar una reserva.")
                return

            reserva = self.tabla_reservas.item(seleccion)["values"]  # Obtener los valores de la reserva seleccionada
            estado = self.estado_actual.get()
            check_box_puntos = self.checkbox_puntos.get()
            numero_habitacion = reserva[2]  # Suponiendo que la columna 2 es el número de la habitación

            # Crear instancia del repositorio de habitaciones
            habitacion_repo = HabitacionRepository(self.db)

            # Check-In
            if estado == "Check-In":
                # Actualizar el estado de la habitación a "Ocupada"
                habitacion = habitacion_repo.get_by_id(numero_habitacion)
                if habitacion:
                    habitacion.estado = "Ocupada"
                    filas_actualizadas = habitacion_repo.update(numero_habitacion, habitacion)
                    if filas_actualizadas > 0:
                        messagebox.showinfo("Check-In", f"Check-In registrado para la reserva {reserva[0]}.\n"
                                                        f"Habitación {numero_habitacion} marcada como 'Ocupada'.")
                    else:
                        messagebox.showerror("Error",
                                             f"No se pudo actualizar el estado de la habitación {numero_habitacion}.")
                else:
                    messagebox.showerror("Error",
                                         f"No se encontró la habitación {numero_habitacion} en la base de datos.")

            # Check-Out
            elif estado == "Check-Out":
                # Obtener la reserva y la habitación para calcular la factura
                reserva_repo = ReservaRepository(self.db)
                reserva_data = reserva_repo.get_reserva_chek_in_out(id_reserva=reserva[0])


                if reserva_data:
                    reserva_obj, _ = reserva_data[0]

                    # Obtener el precio por noche de la habitación
                    habitacion = habitacion_repo.get_by_id(reserva_obj.habitacion)
                    if habitacion:
                        # Calcular el total de la factura (precio por noche * cantidad de noches)
                        noches = (datetime.strptime(reserva_obj.fecha_salida, '%d/%m/%Y') - datetime.strptime(reserva_obj.fecha_entrada,'%d/%m/%Y')).days

                        dict_habitaciones = {
                            'Simple': 5,
                            'Doble': 10,
                            'Suite': 20
                        }
                        tipo_habitacion = habitacion.tipo
                        puntos_habitacion = dict_habitaciones.get(tipo_habitacion)
                        cliente_sv = ClienteService(self.db)
                        cliente_sv.acumular_puntos(id_cliente=reserva[1], puntos=puntos_habitacion * noches)
                        total_factura = (habitacion.precio_por_noche * noches) - (puntos_habitacion * noches if check_box_puntos else 0)

                        # Crear la factura
                        factura = Factura(
                            id_factura=None,  # El ID se generará automáticamente
                            cliente=reserva_obj.cliente,
                            reserva=reserva_obj.id_reserva,
                            fecha_emision=datetime.now().strftime("%d/%m/%Y"),
                            total=total_factura # Asignamos el total calculado a la factura
                        )

                        # Insertar la factura en la base de datos
                        factura_repo = FacturaRepository(self.db)
                        factura_id = factura_repo.create(factura)

                        # Si la factura se creó correctamente
                        if factura_id:
                            # Actualizar el estado de la habitación a "Disponible"
                            habitacion.estado = "Disponible"
                            filas_actualizadas = habitacion_repo.update(reserva_obj.habitacion, habitacion)

                            if filas_actualizadas > 0:
                                messagebox.showinfo("Check-Out",
                                                    f"Check-Out registrado para la reserva {reserva_obj.id_reserva}.\n"
                                                    f"Habitación {numero_habitacion} marcada como 'Disponible'.\n"
                                                    f"Factura generada con ID: {factura_id}")
                            else:
                                messagebox.showerror("Error",
                                                     f"No se pudo actualizar el estado de la habitación {numero_habitacion}.")
                        else:
                            messagebox.showerror("Error", "No se pudo generar la factura.")
                    else:
                        messagebox.showerror("Error", f"No se encontró la habitación {numero_habitacion}.")
                else:
                    messagebox.showerror("Error", f"No se encontró la reserva con ID {reserva[0]}.")

            # Actualizar la tabla después de realizar la acción
            self.actualizar_tabla()

        except Exception as e:
            messagebox.showerror("Error", f"Error al realizar la acción: {e}")


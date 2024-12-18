import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from reportes.factura_Service_2 import generar_factura

from repositories.cliente_repository import ClienteRepository
from repositories.reserva_repository import ReservaRepository
from repositories.habitacion_repository import HabitacionRepository
from repositories.factura_repositoy import FacturaRepository
from clases.factura import Factura
from services.cliente_service import ClienteService

from PIL import Image, ImageTk


class CheckInOut(ctk.CTkToplevel):
    def __init__(self, db):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.db = db
        self.title("Check-In y Check-Out")
        self.geometry("1100x800")
        self.minsize(1100, 800)

        # Cargar imagen de fondo
        self.bg_image = ctk.CTkImage(Image.open("recursos/foto_fondo.jpg"), size=(1100, 800))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image)
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        # Variables para la lógica
        self.opciones_combobox = ["Check-In", "Check-Out"]
        self.estado_actual = tk.StringVar(value=self.opciones_combobox[0])  # Estado inicial: Check-In
        self.dni_filtro = tk.StringVar()
        self.usar_puntos = tk.BooleanVar(value=False)  # Variable para el estado del checkbox

        # Crear widgets de la interfaz
        self.crear_widgets()


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

    def crear_widgets(self):
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(fill="both", expand=False, padx=30, pady=30)

        # Título
        ctk.CTkLabel(frame, text="Check-In y Check-Out", font=("Arial", 18)).pack(pady=20)

        # Combobox para seleccionar Check-In o Check-Out
        ctk.CTkLabel(frame, text="Seleccione una opción:", font=("Arial", 14)).pack(pady=5)
        self.combobox_estado = ctk.CTkComboBox(frame, values=self.opciones_combobox, variable=self.estado_actual,
                                               font=("Arial", 14), state='readonly')
        self.combobox_estado.pack(pady=5)
        self.combobox_estado.bind("<<ComboboxSelected>>", self.actualizar_tabla)

        # Campo para filtrar por DNI
        vcmd_dni = self.register(self.validar_num_rango)

        # Campo para filtrar por DNI
        ctk.CTkLabel(frame, text="Filtrar por DNI:", font=("Arial", 14)).pack(pady=10)
        filtro_frame = ctk.CTkFrame(frame, corner_radius=0)
        filtro_frame.pack(pady=5)
        ctk.CTkEntry(filtro_frame, textvariable=self.dni_filtro, width=300, font=("Arial", 14), validate="key",
                     validatecommand=(vcmd_dni, "%P", 8)).pack(side="left",
                                                               padx=5)

        # Tabla para mostrar las reservas
        self.tabla_reservas = ttk.Treeview(frame, columns=("id_reserva", "cliente", "habitacion", "fecha", "estado"),
                                           show="headings", height=10)  # Limitar la altura
        self.tabla_reservas.heading("id_reserva", text="ID Reserva")
        self.tabla_reservas.heading("cliente", text="Cliente")
        self.tabla_reservas.heading("habitacion", text="Habitación")
        self.tabla_reservas.heading("fecha", text="Fecha")
        self.tabla_reservas.heading("estado", text="Estado")
        self.tabla_reservas.pack(fill="x", pady=20)  # Evitar que se expanda verticalmente

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

        # Botón para volver a la pantalla anterior
        ctk.CTkButton(frame, text="Volver", command=self.destroy,
                      font=("Arial", 14), fg_color="gray", text_color="white", hover_color="#A9A9A9"
                      ).pack(pady=10)

        # Actualizar tabla inicial
        self.actualizar_tabla()

    def fecha_actual(self):
        return datetime.now().date().strftime("%Y-%m-%d")

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
                if (
                           reserva.fecha_salida < fecha_actual or reserva.fecha_entrada <= fecha_actual and reserva.fecha_salida >= fecha_actual) and estado_habitacion == "Ocupada"
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
                        noches = (datetime.strptime(reserva_obj.fecha_salida, "%Y-%m-%d") - datetime.strptime(
                            reserva_obj.fecha_entrada, "%Y-%m-%d")).days

                        dict_habitaciones = {
                            'Simple': 5,
                            'Doble': 10,
                            'Suite': 20,
                            'Salon': 50
                        }
                        tipo_habitacion = habitacion.tipo
                        puntos_habitacion = dict_habitaciones.get(tipo_habitacion)
                        cliente_sv = ClienteService(self.db)
                        cliente_sv.acumular_puntos(id_cliente=reserva[1], puntos=(
                            puntos_habitacion * noches if noches > 0 else puntos_habitacion))
                        cliente_repo = ClienteRepository(self.db)
                        total_puntos = cliente_repo.get_puntos(id_cliente=reserva[1])
                        puntos_menor_que_precio = True if total_puntos <= habitacion.precio_por_noche * noches else False
                        if puntos_menor_que_precio:
                            cliente_sv.canjear_puntos(id_cliente=reserva[1],
                                                      puntos_a_canjear=total_puntos) if check_box_puntos else ''
                        total_factura = (
                                            habitacion.precio_por_noche * noches if noches else habitacion.precio_por_noche) - (
                                            total_puntos if check_box_puntos and puntos_menor_que_precio else 0)

                        if self.fecha_actual() < (reserva[4]):
                            reserva_a_modificar = reserva_repo.get_by_id(reserva[0])
                            reserva_a_modificar.fecha_salida = self.fecha_actual()
                            reserva_repo.update(reserva[0], reserva_a_modificar)
                        # Crear la factura
                        factura = Factura(
                            id_factura=None,  # El ID se generará automáticamente
                            cliente=reserva_obj.cliente,
                            reserva=reserva_obj.id_reserva,
                            fecha_emision=datetime.now().date().strftime("%Y-%m-%d"),
                            total=total_factura  # Asignamos el total calculado a la factura
                        )

                        # Insertar la factura en la base de datos
                        factura_repo = FacturaRepository(self.db)
                        factura_id = factura_repo.create(factura)

                        # Si la factura se creó correctamente
                        if factura_id:
                            nombre_cliente = cliente_repo.get_by_dni(dni=reserva[1])
                            descripcion_factura = f'Estadia Habitación {tipo_habitacion}'
                            item = [habitacion.numero, descripcion_factura, float(habitacion.precio_por_noche),
                                    float(total_factura)]
                            generar_factura(facturar_a=f'{nombre_cliente.nombre} {nombre_cliente.apellido}',
                                            numero_factura=factura_id, fecha=self.fecha_actual(),
                                            fecha_vencimiento=self.fecha_actual(), items=[item],
                                            subtotal=float(total_factura),
                                            iva=21.00, total=float(total_factura*1.21))
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

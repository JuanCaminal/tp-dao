import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Habitacion:
    def __init__(self, numero, tipo, estado="disponible", precio_por_noche=0):
        self.numero = numero
        self.tipo = tipo
        self.estado = estado
        self.precio_por_noche = precio_por_noche

class Cliente:
    def __init__(self, id_cliente, nombre, apellido, direccion, telefono, email):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.telefono = telefono
        self.email = email

class Reserva:
    def __init__(self, id_reserva, cliente, habitacion, fecha_entrada, fecha_salida, cantidad_personas):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.habitacion = habitacion
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.cantidad_personas = cantidad_personas

class SistemaHotel:
    def __init__(self):
        self.reservas = []

    def agregar_reserva(self, reserva):
        self.reservas.append(reserva)

    def listar_reservas_periodo(self, fecha_inicio, fecha_fin):
        return [
            reserva for reserva in self.reservas
            if reserva.fecha_entrada >= fecha_inicio and reserva.fecha_salida <= fecha_fin
        ]

# Crear el sistema y añadir algunas reservas de ejemplo
sistema_hotel = SistemaHotel()
cliente1 = Cliente(1, "Juan", "Pérez", "Calle 123", "555-1234", "juan.perez@mail.com")
habitacion1 = Habitacion(101, "doble", precio_por_noche=80)
reserva1 = Reserva(1, cliente1, habitacion1, datetime(2024, 10, 20), datetime(2024, 10, 25), 2)
sistema_hotel.agregar_reserva(reserva1)

# Interfaz gráfica
def mostrar_reservas():
    try:
        fecha_inicio = datetime.strptime(entry_fecha_inicio.get(), "%Y-%m-%d")
        fecha_fin = datetime.strptime(entry_fecha_fin.get(), "%Y-%m-%d")
        reservas_periodo = sistema_hotel.listar_reservas_periodo(fecha_inicio, fecha_fin)

        resultado = "Reservas:\n"
        if reservas_periodo:
            for reserva in reservas_periodo:
                resultado += f"ID: {reserva.id_reserva}, Cliente: {reserva.cliente.nombre} {reserva.cliente.apellido}, Habitación: {reserva.habitacion.numero}, Entrada: {reserva.fecha_entrada}, Salida: {reserva.fecha_salida}\n"
        else:
            resultado += "No hay reservas en este período."
        messagebox.showinfo("Reporte de Reservas", resultado)
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa las fechas en el formato YYYY-MM-DD.")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Gestión de Hotel")
ventana.geometry("400x200")

# Etiquetas y campos de entrada para las fechas
tk.Label(ventana, text="Fecha de inicio (YYYY-MM-DD):").pack(pady=5)
entry_fecha_inicio = tk.Entry(ventana)
entry_fecha_inicio.pack()

tk.Label(ventana, text="Fecha de fin (YYYY-MM-DD):").pack(pady=5)
entry_fecha_fin = tk.Entry(ventana)
entry_fecha_fin.pack()

# Botón para mostrar el reporte de reservas
btn_mostrar_reservas = tk.Button(ventana, text="Mostrar Reservas", command=mostrar_reservas)
btn_mostrar_reservas.pack(pady=10)

ventana.mainloop()

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from pathlib import Path
from config.constantes import RUTA_ICONO_UTN




ruta_icono = RUTA_ICONO_UTN
# Clases base para el sistema
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

    def duracion_estancia(self):
        return (self.fecha_salida - self.fecha_entrada).days

class SistemaHotel:
    def __init__(self):
        self.reservas = []

    def agregar_reserva(self, reserva):
        self.reservas.append(reserva)

    def ingresos_por_habitacion(self, fecha_inicio, fecha_fin):
        ingresos = {}
        for reserva in self.reservas:
            if reserva.fecha_entrada >= fecha_inicio and reserva.fecha_salida <= fecha_fin:
                duracion = reserva.duracion_estancia()
                ingreso_reserva = duracion * reserva.habitacion.precio_por_noche
                if reserva.habitacion.numero in ingresos:
                    ingresos[reserva.habitacion.numero] += ingreso_reserva
                else:
                    ingresos[reserva.habitacion.numero] = ingreso_reserva
        return ingresos

# Crear el sistema y añadir reservas de ejemplo
sistema_hotel = SistemaHotel()
cliente1 = Cliente(1, "Juan", "Pérez", "Calle 123", "555-1234", "juan.perez@mail.com")
habitacion1 = Habitacion(101, "doble", precio_por_noche=80)
habitacion2 = Habitacion(300, "triple", precio_por_noche=90)
reserva1 = Reserva(1, cliente1, habitacion1, datetime(2024, 10, 20), datetime(2024, 10, 25), 2)
reserva2 = Reserva(1, cliente1, habitacion2, datetime(2024, 10, 19), datetime(2024, 10, 26), 2)
sistema_hotel.agregar_reserva(reserva1)
sistema_hotel.agregar_reserva(reserva2)

# Interfaz gráfica
def mostrar_ingresos():
    try:
        fecha_inicio = datetime.strptime(entry_fecha_inicio.get(), "%Y-%m-%d")
        fecha_fin = datetime.strptime(entry_fecha_fin.get(), "%Y-%m-%d")
        ingresos = sistema_hotel.ingresos_por_habitacion(fecha_inicio, fecha_fin)

        resultado = "Ingresos por habitación:\n"
        if ingresos:
            for habitacion, ingreso in ingresos.items():
                resultado += f"Habitación {habitacion}: ${ingreso:.2f}\n"
        else:
            resultado += "No se generaron ingresos en este período."
        messagebox.showinfo("Reporte de Ingresos", resultado)
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa las fechas en el formato YYYY-MM-DD.")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Gestión de Hotel")
ventana.geometry("400x200")
ventana.iconbitmap(ruta_icono)

# Etiquetas y campos de entrada para las fechas
tk.Label(ventana, text="Fecha de inicio (YYYY-MM-DD):").pack(pady=5)
entry_fecha_inicio = tk.Entry(ventana)
entry_fecha_inicio.pack()

tk.Label(ventana, text="Fecha de fin (YYYY-MM-DD):").pack(pady=5)
entry_fecha_fin = tk.Entry(ventana)
entry_fecha_fin.pack()

# Botón para mostrar el reporte de ingresos
btn_mostrar_ingresos = tk.Button(ventana, text="Mostrar Ingresos", command=mostrar_ingresos)
btn_mostrar_ingresos.pack(pady=10)

ventana.mainloop()

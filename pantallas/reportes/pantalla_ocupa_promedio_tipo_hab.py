import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry

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

    def ocupacion_promedio_por_tipo(self, fecha_inicio, fecha_fin):
        ocupacion = {}
        total_dias = (fecha_fin - fecha_inicio).days

        # Contar reservas por tipo de habitación
        for reserva in self.reservas:
            if reserva.fecha_entrada < fecha_fin and reserva.fecha_salida > fecha_inicio:
                tipo = reserva.habitacion.tipo
                if tipo in ocupacion:
                    ocupacion[tipo] += reserva.duracion_estancia()
                else:
                    ocupacion[tipo] = reserva.duracion_estancia()

        # Calcular ocupación promedio
        promedio_ocupacion = {tipo: dias / total_dias for tipo, dias in ocupacion.items()}
        return promedio_ocupacion

# Crear el sistema y añadir reservas de ejemplo
sistema_hotel = SistemaHotel()

# Crear clientes
cliente1 = Cliente(1, "Juan", "Pérez", "Calle 123", "555-1234", "juan.perez@mail.com")
cliente2 = Cliente(2, "Ana", "Gómez", "Calle 456", "555-5678", "ana.gomez@mail.com")
cliente3 = Cliente(3, "Luis", "Martínez", "Calle 789", "555-9101", "luis.martinez@mail.com")

# Crear habitaciones
habitacion1 = Habitacion(101, "doble", precio_por_noche=80)
habitacion2 = Habitacion(102, "simple", precio_por_noche=50)
habitacion3 = Habitacion(103, "suite", precio_por_noche=120)

# Crear reservas
reserva1 = Reserva(1, cliente1, habitacion1, datetime(2024, 10, 20), datetime(2024, 10, 25), 2)
reserva2 = Reserva(2, cliente2, habitacion2, datetime(2024, 10, 22), datetime(2024, 10, 27), 1)
reserva3 = Reserva(3, cliente3, habitacion3, datetime(2024, 10, 24), datetime(2024, 10, 29), 3)

# Agregar reservas al sistema
sistema_hotel.agregar_reserva(reserva1)
sistema_hotel.agregar_reserva(reserva2)
sistema_hotel.agregar_reserva(reserva3)

# Interfaz gráfica
def mostrar_ocupacion_promedio():
    try:
        fecha_inicio = datetime.strptime(entry_fecha_inicio.get(), "%Y-%m-%d")
        fecha_fin = datetime.strptime(entry_fecha_fin.get(), "%Y-%m-%d")
        ocupacion_promedio = sistema_hotel.ocupacion_promedio_por_tipo(fecha_inicio, fecha_fin)

        # Limpiar el árbol antes de agregar nuevos datos
        for i in tree.get_children():
            tree.delete(i)

        if ocupacion_promedio:
            for tipo, promedio in ocupacion_promedio.items():
                tree.insert("", "end", values=(tipo, f"{promedio:.2%}"))
        else:
            messagebox.showinfo("Reporte de Ocupación Promedio", "No hay datos para mostrar.")
    except ValueError:
        messagebox.showerror("Error", "Por favor selecciona fechas válidas.")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Gestión de Hotel")
ventana.geometry("400x300")

# Etiquetas y campos de entrada de fecha
tk.Label(ventana, text="Fecha de inicio:").pack(pady=5)
entry_fecha_inicio = DateEntry(ventana, width=12, background="darkblue", foreground="white", date_pattern="yyyy-MM-dd")
entry_fecha_inicio.pack()

tk.Label(ventana, text="Fecha de fin:").pack(pady=5)
entry_fecha_fin = DateEntry(ventana, width=12, background="darkblue", foreground="white", date_pattern="yyyy-MM-dd")
entry_fecha_fin.pack()

# Botón para mostrar el reporte de ocupación promedio
btn_mostrar_ocupacion = tk.Button(ventana, text="Mostrar Ocupación Promedio", command=mostrar_ocupacion_promedio)
btn_mostrar_ocupacion.pack(pady=10)

# Crear el Treeview para mostrar la ocupación
columns = ("Tipo", "Ocupación")
tree = ttk.Treeview(ventana, columns=columns, show="headings")
tree.heading("Tipo", text="Tipo de Habitación")
tree.heading("Ocupación", text="Ocupación Promedio")
tree.pack(pady=10, fill=tk.BOTH, expand=True)

ventana.mainloop()

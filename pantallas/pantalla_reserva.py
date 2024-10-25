import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Clases necesarias
class Cliente:
    def __init__(self, id_cliente, nombre, apellido, direccion, telefono, email):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.telefono = telefono
        self.email = email

class Habitacion:
    def __init__(self, numero, tipo, estado, precio_por_noche):
        self.numero = numero
        self.tipo = tipo
        self.estado = estado
        self.precio_por_noche = precio_por_noche

class Reserva:
    def __init__(self, id_reserva, cliente, habitacion, fecha_entrada, fecha_salida, cantidad_personas):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.habitacion = habitacion
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.cantidad_personas = cantidad_personas

# Listas de ejemplo para clientes y habitaciones
clientes = [
    Cliente("1", "Juan", "Perez", "Calle Falsa 123", "123456789", "juan@example.com"),
    Cliente("2", "Ana", "Garcia", "Avenida Siempre Viva 456", "987654321", "ana@example.com")
]

habitaciones = [
    Habitacion("101", "Simple", "Disponible", 50),
    Habitacion("102", "Doble", "Ocupada", 80),
    Habitacion("103", "Suite", "Disponible", 120)
]

# Lista para almacenar reservas
reservas = []

# Función para registrar una reserva
def registrar_reserva():
    id_reserva = entry_id_reserva.get()
    cliente = cliente_var.get()
    habitacion = habitacion_var.get()
    fecha_entrada = entry_fecha_entrada.get()
    fecha_salida = entry_fecha_salida.get()
    cantidad_personas = entry_cantidad_personas.get()

    # Validaciones
    if not (id_reserva and cliente and habitacion and fecha_entrada and fecha_salida and cantidad_personas):
        messagebox.showerror("Error", "Debe completar todos los campos")
        return

    # Convertir fechas y validar orden de entrada/salida
    try:
        fecha_entrada_dt = datetime.strptime(fecha_entrada, "%Y-%m-%d")
        fecha_salida_dt = datetime.strptime(fecha_salida, "%Y-%m-%d")
        if fecha_entrada_dt >= fecha_salida_dt:
            messagebox.showerror("Error", "La fecha de salida debe ser posterior a la de entrada")
            return
    except ValueError:
        messagebox.showerror("Error", "Formato de fecha inválido. Use AAAA-MM-DD")
        return

    # Crear la reserva y agregarla a la lista
    reserva = Reserva(id_reserva, cliente, habitacion, fecha_entrada, fecha_salida, cantidad_personas)
    reservas.append(reserva)

    # Limpiar campos de entrada
    entry_id_reserva.delete(0, tk.END)
    cliente_var.set("")
    habitacion_var.set("")
    entry_fecha_entrada.delete(0, tk.END)
    entry_fecha_salida.delete(0, tk.END)
    entry_cantidad_personas.delete(0, tk.END)

    # Actualizar la tabla de reservas
    actualizar_tabla_reservas()

# Función para actualizar la tabla de reservas
def actualizar_tabla_reservas():
    for row in tabla_reservas.get_children():
        tabla_reservas.delete(row)
    for reserva in reservas:
        tabla_reservas.insert("", "end", values=(reserva.id_reserva, reserva.cliente, reserva.habitacion,
                                                 reserva.fecha_entrada, reserva.fecha_salida, reserva.cantidad_personas))

# Crear ventana para Reservas
root_reserva = tk.Tk()
root_reserva.title("Registro de Reservas")

# Etiquetas y campos de entrada
tk.Label(root_reserva, text="ID Reserva:").grid(row=0, column=0, padx=10, pady=10)
entry_id_reserva = tk.Entry(root_reserva)
entry_id_reserva.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root_reserva, text="Cliente:").grid(row=1, column=0, padx=10, pady=10)
cliente_var = tk.StringVar()
combo_cliente = ttk.Combobox(root_reserva, textvariable=cliente_var, values=[f"{cliente.id_cliente} - {cliente.nombre}" for cliente in clientes])
combo_cliente.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root_reserva, text="Habitación:").grid(row=2, column=0, padx=10, pady=10)
habitacion_var = tk.StringVar()
combo_habitacion = ttk.Combobox(root_reserva, textvariable=habitacion_var, values=[f"{habitacion.numero} - {habitacion.tipo}" for habitacion in habitaciones if habitacion.estado == "Disponible"])
combo_habitacion.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root_reserva, text="Fecha de Entrada (AAAA-MM-DD):").grid(row=3, column=0, padx=10, pady=10)
entry_fecha_entrada = tk.Entry(root_reserva)
entry_fecha_entrada.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root_reserva, text="Fecha de Salida (AAAA-MM-DD):").grid(row=4, column=0, padx=10, pady=10)
entry_fecha_salida = tk.Entry(root_reserva)
entry_fecha_salida.grid(row=4, column=1, padx=10, pady=10)

tk.Label(root_reserva, text="Cantidad de Personas:").grid(row=5, column=0, padx=10, pady=10)
entry_cantidad_personas = tk.Entry(root_reserva)
entry_cantidad_personas.grid(row=5, column=1, padx=10, pady=10)

# Botón para registrar reserva
btn_registrar_reserva = tk.Button(root_reserva, text="Registrar Reserva", command=registrar_reserva)
btn_registrar_reserva.grid(row=6, column=0, columnspan=2, pady=10)

# Tabla para mostrar las reservas registradas
tabla_reservas = ttk.Treeview(root_reserva, columns=("id_reserva", "cliente", "habitacion", "fecha_entrada", "fecha_salida", "cantidad_personas"), show="headings")
tabla_reservas.heading("id_reserva", text="ID Reserva")
tabla_reservas.heading("cliente", text="Cliente")
tabla_reservas.heading("habitacion", text="Habitación")
tabla_reservas.heading("fecha_entrada", text="Fecha de Entrada")
tabla_reservas.heading("fecha_salida", text="Fecha de Salida")
tabla_reservas.heading("cantidad_personas", text="Personas")
tabla_reservas.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Iniciar loop
root_reserva.mainloop()

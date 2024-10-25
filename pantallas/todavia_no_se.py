import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Listas para almacenar clientes, habitaciones, reservas y empleados
clientes = [("1", "Juan Pérez"), ("2", "María Gómez")]
habitaciones = [("101", "Simple"), ("102", "Doble")]
reservas = []
empleados = [("1", "Pedro López"), ("2", "Ana Torres")]

# Clase Reserva
class Reserva:
    def __init__(self, id_reserva, cliente, habitacion, fecha_entrada, fecha_salida, cantidad_personas):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.habitacion = habitacion
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.cantidad_personas = cantidad_personas

# Función para registrar una reserva
def registrar_reserva():
    id_reserva = entry_id_reserva.get()
    cliente = combo_cliente.get().split(" - ")[0]
    habitacion = combo_habitacion.get().split(" - ")[0]
    fecha_entrada = entry_fecha_entrada.get()
    fecha_salida = entry_fecha_salida.get()
    cantidad_personas = entry_cantidad_personas.get()

    # Validaciones
    if not (id_reserva and cliente and habitacion and fecha_entrada and fecha_salida and cantidad_personas):
        messagebox.showerror("Error", "Debe completar todos los campos")
        return

    try:
        fecha_entrada = datetime.strptime(fecha_entrada, "%Y-%m-%d")
        fecha_salida = datetime.strptime(fecha_salida, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Las fechas deben estar en formato YYYY-MM-DD")
        return

    reserva = Reserva(id_reserva, cliente, habitacion, fecha_entrada, fecha_salida, cantidad_personas)
    reservas.append(reserva)
    actualizar_tabla_reservas()
    limpiar_campos_reserva()

def limpiar_campos_reserva():
    entry_id_reserva.delete(0, tk.END)
    entry_fecha_entrada.delete(0, tk.END)
    entry_fecha_salida.delete(0, tk.END)
    entry_cantidad_personas.delete(0, tk.END)

def actualizar_tabla_reservas():
    for row in tabla_reservas.get_children():
        tabla_reservas.delete(row)
    for reserva in reservas:
        tabla_reservas.insert("", "end", values=(reserva.id_reserva, reserva.cliente, reserva.habitacion, reserva.fecha_entrada.date(), reserva.fecha_salida.date(), reserva.cantidad_personas))

# Función para generar factura
def generar_factura():
    if not reservas:
        messagebox.showerror("Error", "No hay reservas registradas")
        return

    reserva = reservas[-1]
    total = calcular_total(reserva)
    factura = {
        "id_factura": f"F-{reserva.id_reserva}",
        "cliente": reserva.cliente,
        "fecha_emision": datetime.now(),
        "total": total,
    }

    messagebox.showinfo("Factura Generada", f"Factura ID: {factura['id_factura']}\nCliente: {factura['cliente']}\nTotal: ${factura['total']:.2f}")

def calcular_total(reserva):
    precio_habitacion = 100  # Ejemplo, reemplaza con el precio real
    dias = (reserva.fecha_salida - reserva.fecha_entrada).days
    return precio_habitacion * dias

# Función para asignar empleado a habitación
def asignar_empleado_habitacion():
    empleado = combo_empleado.get()
    habitacion = combo_habitacion_empleado.get()

    if not (empleado and habitacion):
        messagebox.showerror("Error", "Debe seleccionar un empleado y una habitación")
        return

    messagebox.showinfo("Asignación Exitosa", f"Empleado {empleado} asignado a la habitación {habitacion}")

# Función para consultar disponibilidad de habitaciones
def consultar_disponibilidad():
    fecha_entrada = entry_fecha_entrada_consulta.get()
    fecha_salida = entry_fecha_salida_consulta.get()

    if not (fecha_entrada and fecha_salida):
        messagebox.showerror("Error", "Debe completar ambas fechas")
        return

    try:
        fecha_entrada = datetime.strptime(fecha_entrada, "%Y-%m-%d")
        fecha_salida = datetime.strptime(fecha_salida, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Las fechas deben estar en formato YYYY-MM-DD")
        return

    habitaciones_disponibles = [h for h in habitaciones if h[0] not in [reserva.habitacion for reserva in reservas if reserva.fecha_entrada < fecha_salida and reserva.fecha_salida > fecha_entrada]]
    if habitaciones_disponibles:
        mensaje = "Habitaciones disponibles:\n" + "\n".join([f"{h[0]} - {h[1]}" for h in habitaciones_disponibles])
    else:
        mensaje = "No hay habitaciones disponibles."

    messagebox.showinfo("Disponibilidad", mensaje)

# Crear la ventana para el Registro de Reservas
root = tk.Tk()
root.title("Sistema de Gestión de Hotel")

# Sección Registro de Reservas
frame_reserva = tk.Frame(root)
frame_reserva.pack(padx=10, pady=10)

tk.Label(frame_reserva, text="ID Reserva:").grid(row=0, column=0, padx=10, pady=10)
entry_id_reserva = tk.Entry(frame_reserva)
entry_id_reserva.grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame_reserva, text="Cliente:").grid(row=1, column=0, padx=10, pady=10)
combo_cliente = ttk.Combobox(frame_reserva, values=[f"{id} - {nombre}" for id, nombre in clientes])
combo_cliente.grid(row=1, column=1, padx=10, pady=10)

tk.Label(frame_reserva, text="Habitación:").grid(row=2, column=0, padx=10, pady=10)
combo_habitacion = ttk.Combobox(frame_reserva, values=[f"{id} - {tipo}" for id, tipo in habitaciones])
combo_habitacion.grid(row=2, column=1, padx=10, pady=10)

tk.Label(frame_reserva, text="Fecha de Entrada (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=10)
entry_fecha_entrada = tk.Entry(frame_reserva)
entry_fecha_entrada.grid(row=3, column=1, padx=10, pady=10)

tk.Label(frame_reserva, text="Fecha de Salida (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=10)
entry_fecha_salida = tk.Entry(frame_reserva)
entry_fecha_salida.grid(row=4, column=1, padx=10, pady=10)

tk.Label(frame_reserva, text="Cantidad de Personas:").grid(row=5, column=0, padx=10, pady=10)
entry_cantidad_personas = tk.Entry(frame_reserva)
entry_cantidad_personas.grid(row=5, column=1, padx=10, pady=10)

btn_registrar_reserva = tk.Button(frame_reserva, text="Registrar Reserva", command=registrar_reserva)
btn_registrar_reserva.grid(row=6, column=0, columnspan=2, pady=10)

# Tabla para mostrar reservas
tabla_reservas = ttk.Treeview(frame_reserva, columns=("id_reserva", "cliente", "habitacion", "fecha_entrada", "fecha_salida", "cantidad_personas"), show="headings")
tabla_reservas.heading("id_reserva", text="ID Reserva")
tabla_reservas.heading("cliente", text="Cliente")
tabla_reservas.heading("habitacion", text="Habitación")
tabla_reservas.heading("fecha_entrada", text="Fecha Entrada")
tabla_reservas.heading("fecha_salida", text="Fecha Salida")
tabla_reservas.heading("cantidad_personas", text="Cantidad de Personas")
tabla_reservas.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Botón para generar factura
btn_generar_factura = tk.Button(frame_reserva, text="Generar Factura", command=generar_factura)
btn_generar_factura.grid(row=8, column=0, columnspan=2, pady=10)

# Sección Asignación de Empleados
frame_empleado = tk.Frame(root)
frame_empleado.pack(padx=10, pady=10)

tk.Label(frame_empleado, text="Empleado:").grid(row=0, column=0, padx=10, pady=10)
combo_empleado = ttk.Combobox(frame_empleado, values=[f"{id} - {nombre}" for id, nombre in empleados])
combo_empleado.grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame_empleado, text="Habitación:").grid(row=1, column=0, padx=10, pady=10)
combo_habitacion_empleado = ttk.Combobox(frame_empleado, values=[f"{id} - {tipo}" for id, tipo in habitaciones])
combo_habitacion_empleado.grid(row=1, column=1, padx=10, pady=10)

btn_asignar_empleado = tk.Button(frame_empleado, text="Asignar Empleado", command=asignar_empleado_habitacion)
btn_asignar_empleado.grid(row=2, column=0, columnspan=2, pady=10)

# Sección Consulta de Disponibilidad
frame_disponibilidad = tk.Frame(root)
frame_disponibilidad.pack(padx=10, pady=10)

tk.Label(frame_disponibilidad, text="Fecha de Entrada (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
entry_fecha_entrada_consulta = tk.Entry(frame_disponibilidad)
entry_fecha_entrada_consulta.grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame_disponibilidad, text="Fecha de Salida (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)
entry_fecha_salida_consulta = tk.Entry(frame_disponibilidad)
entry_fecha_salida_consulta.grid(row=1, column=1, padx=10, pady=10)

btn_consultar_disponibilidad = tk.Button(frame_disponibilidad, text="Consultar Disponibilidad", command=consultar_disponibilidad)
btn_consultar_disponibilidad.grid(row=2, column=0, columnspan=2, pady=10)

# Iniciar el loop de la ventana
root.mainloop()

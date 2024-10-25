# asignacion_empleados.py

import tkinter as tk
from tkinter import ttk, messagebox

# Clase Empleado
class Empleado:
    def __init__(self, id_empleado, nombre, apellido, cargo):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.apellido = apellido
        self.cargo = cargo

# Clase Habitacion
class Habitacion:
    def __init__(self, numero, tipo):
        self.numero = numero
        self.tipo = tipo
        self.empleado_asignado = None

# Listas de empleados y habitaciones de ejemplo
empleados = [
    Empleado(1, "Juan", "Pérez", "Recepcionista"),
    Empleado(2, "María", "Gómez", "Servicio de Limpieza"),
    Empleado(3, "Carlos", "López", "Servicio de Limpieza"),
]

habitaciones = [
    Habitacion(101, "Doble"),
    Habitacion(102, "Suite"),
    Habitacion(103, "Simple"),
]

# Función para asignar empleado a habitación
def asignar_empleado(habitacion_var, empleado_var):
    empleado = empleado_var.get()
    habitacion = habitacion_var.get()

    if not empleado or not habitacion:
        messagebox.showerror("Error", "Por favor, seleccione un empleado y una habitación.")
        return

    # Asignar empleado a la habitación
    for hab in habitaciones:
        if f"{hab.numero} - {hab.tipo}" == habitacion:
            hab.empleado_asignado = empleado
            messagebox.showinfo("Éxito", f"Empleado {empleado} asignado a la habitación {hab.numero}.")
            return

# Crear interfaz para asignar empleados a habitaciones
def crear_interfaz_asignacion():
    root = tk.Tk()
    root.title("Asignación de Empleados a Habitaciones")

    frame_asignacion = tk.Frame(root)
    frame_asignacion.pack(padx=10, pady=10)

    tk.Label(frame_asignacion, text="Asignación de Empleados a Habitaciones").grid(row=0, column=0, columnspan=2)

    # Combobox de Empleados
    tk.Label(frame_asignacion, text="Empleado:").grid(row=1, column=0)
    empleado_var = tk.StringVar()
    combo_empleado = ttk.Combobox(frame_asignacion, textvariable=empleado_var,
                                   values=[f"{empleado.id_empleado} - {empleado.nombre} {empleado.apellido}" for empleado in empleados])
    combo_empleado.grid(row=1, column=1)

    # Combobox de Habitaciones
    tk.Label(frame_asignacion, text="Habitación:").grid(row=2, column=0)
    habitacion_var = tk.StringVar()
    combo_habitacion = ttk.Combobox(frame_asignacion, textvariable=habitacion_var,
                                     values=[f"{hab.numero} - {hab.tipo}" for hab in habitaciones])
    combo_habitacion.grid(row=2, column=1)

    # Botón para asignar empleado
    btn_asignar_empleado = tk.Button(frame_asignacion, text="Asignar Empleado", command=lambda: asignar_empleado(habitacion_var, empleado_var))
    btn_asignar_empleado.grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()

# Ejecutar la interfaz de asignación
if __name__ == "__main__":
    crear_interfaz_asignacion()

import tkinter as tk
from tkinter import ttk, messagebox

# Clase básica para la entidad Habitación
class Habitacion:
    def __init__(self, numero, tipo, estado, precio_por_noche):
        self.numero = numero
        self.tipo = tipo
        self.estado = estado
        self.precio_por_noche = precio_por_noche

# Lista para almacenar habitaciones
habitaciones = []

# Función para registrar una habitación
def registrar_habitacion():
    numero = entry_numero.get()
    tipo = tipo_var.get()
    estado = estado_var.get()
    precio = entry_precio.get()
    
    # Validaciones simples
    if not numero or not precio:
        messagebox.showerror("Error", "Debe completar todos los campos")
        return
    
    # Crear la instancia de la habitación y agregarla a la lista
    habitacion = Habitacion(numero, tipo, estado, precio)
    habitaciones.append(habitacion)
    
    # Limpiar los campos
    entry_numero.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    tipo_var.set("Simple")
    estado_var.set("Disponible")
    
    # Actualizar la tabla
    actualizar_tabla()

# Función para actualizar la tabla de habitaciones
def actualizar_tabla():
    for row in tabla.get_children():
        tabla.delete(row)
    for habitacion in habitaciones:
        tabla.insert("", "end", values=(habitacion.numero, habitacion.tipo, habitacion.estado, habitacion.precio_por_noche))

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Gestión de Hotel - Registro de Habitaciones")

# Etiquetas y campos de entrada
tk.Label(root, text="Número de Habitación:").grid(row=0, column=0, padx=10, pady=10)
entry_numero = tk.Entry(root)
entry_numero.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Tipo de Habitación:").grid(row=1, column=0, padx=10, pady=10)
tipo_var = tk.StringVar(value="Simple")
combo_tipo = ttk.Combobox(root, textvariable=tipo_var, values=["Simple", "Doble", "Suite"])
combo_tipo.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Estado:").grid(row=2, column=0, padx=10, pady=10)
estado_var = tk.StringVar(value="Disponible")
combo_estado = ttk.Combobox(root, textvariable=estado_var, values=["Disponible", "Ocupada"])
combo_estado.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Precio por Noche:").grid(row=3, column=0, padx=10, pady=10)
entry_precio = tk.Entry(root)
entry_precio.grid(row=3, column=1, padx=10, pady=10)

# Botón para registrar la habitación
btn_registrar = tk.Button(root, text="Registrar Habitación", command=registrar_habitacion)
btn_registrar.grid(row=4, column=0, columnspan=2, pady=10)

# Tabla para mostrar las habitaciones registradas
tabla = ttk.Treeview(root, columns=("numero", "tipo", "estado", "precio"), show="headings")
tabla.heading("numero", text="Número")
tabla.heading("tipo", text="Tipo")
tabla.heading("estado", text="Estado")
tabla.heading("precio", text="Precio por Noche")
tabla.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Iniciar el loop principal
root.mainloop()

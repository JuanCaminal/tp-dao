import tkinter as tk
from tkinter import ttk, messagebox

# Clase Cliente
class Cliente:
    def __init__(self, id_cliente, nombre, apellido, direccion, telefono, email):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.telefono = telefono
        self.email = email

# Lista para almacenar clientes
clientes = []

# Función para registrar un cliente
def registrar_cliente():
    id_cliente = entry_id.get()
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    direccion = entry_direccion.get()
    telefono = entry_telefono.get()
    email = entry_email.get()
    
    clientes = [
    Cliente("1", "Juan", "Perez", "Calle Falsa 123", "123456789", "juan@example.com"),
    Cliente("2", "Ana", "Garcia", "Avenida Siempre Viva 456", "987654321", "ana@example.com")
    ]

    
    # Validación
    if not (id_cliente and nombre and apellido and direccion and telefono and email):
        messagebox.showerror("Error", "Debe completar todos los campos")
        return
    
    # Crear el cliente y agregarlo a la lista
    cliente = Cliente(id_cliente, nombre, apellido, direccion, telefono, email)
    clientes.append(cliente)
    
    # Limpiar campos de entrada
    entry_id.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    
    # Actualizar la tabla
    actualizar_tabla_clientes()

# Función para actualizar la tabla de clientes
def actualizar_tabla_clientes():
    for row in tabla_clientes.get_children():
        tabla_clientes.delete(row)
    for cliente in clientes:
        tabla_clientes.insert("", "end", values=(cliente.id_cliente, cliente.nombre, cliente.apellido, cliente.direccion, cliente.telefono, cliente.email))

# Crear ventana para Clientes
root_cliente = tk.Tk()
root_cliente.title("Registro de Clientes")

# Etiquetas y campos de entrada
tk.Label(root_cliente, text="ID Cliente:").grid(row=0, column=0, padx=10, pady=10)
entry_id = tk.Entry(root_cliente)
entry_id.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root_cliente, text="Nombre:").grid(row=1, column=0, padx=10, pady=10)
entry_nombre = tk.Entry(root_cliente)
entry_nombre.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root_cliente, text="Apellido:").grid(row=2, column=0, padx=10, pady=10)
entry_apellido = tk.Entry(root_cliente)
entry_apellido.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root_cliente, text="Dirección:").grid(row=3, column=0, padx=10, pady=10)
entry_direccion = tk.Entry(root_cliente)
entry_direccion.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root_cliente, text="Teléfono:").grid(row=4, column=0, padx=10, pady=10)
entry_telefono = tk.Entry(root_cliente)
entry_telefono.grid(row=4, column=1, padx=10, pady=10)

tk.Label(root_cliente, text="Email:").grid(row=5, column=0, padx=10, pady=10)
entry_email = tk.Entry(root_cliente)
entry_email.grid(row=5, column=1, padx=10, pady=10)

# Botón para registrar cliente
btn_registrar_cliente = tk.Button(root_cliente, text="Registrar Cliente", command=registrar_cliente)
btn_registrar_cliente.grid(row=6, column=0, columnspan=2, pady=10)

# Tabla para mostrar los clientes registrados
tabla_clientes = ttk.Treeview(root_cliente, columns=("id_cliente", "nombre", "apellido", "direccion", "telefono", "email"), show="headings")
tabla_clientes.heading("id_cliente", text="ID Cliente")
tabla_clientes.heading("nombre", text="Nombre")
tabla_clientes.heading("apellido", text="Apellido")
tabla_clientes.heading("direccion", text="Dirección")
tabla_clientes.heading("telefono", text="Teléfono")
tabla_clientes.heading("email", text="Email")
tabla_clientes.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Iniciar loop
root_cliente.mainloop()

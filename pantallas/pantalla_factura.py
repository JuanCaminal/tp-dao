# facturacion.py

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Clase Factura
class Factura:
    def __init__(self, id_factura, cliente, reserva, fecha_emision, total):
        self.id_factura = id_factura
        self.cliente = cliente
        self.reserva = reserva
        self.fecha_emision = fecha_emision
        self.total = total

# Lista para almacenar las facturas
facturas = []

# Función para generar factura
def generar_factura(cliente, reserva, fecha_salida):
    total = calcular_total(reserva)  # Suponiendo que hay una función calcular_total definida
    factura = Factura(f"F-{len(facturas) + 1}", cliente, reserva, datetime.now(), total)
    facturas.append(factura)

    # Mostrar información de la factura
    mensaje = f"Factura ID: {factura.id_factura}\nCliente: {factura.cliente}\nTotal: ${factura.total:.2f}"
    messagebox.showinfo("Factura Generada", mensaje)

# Función para calcular el total de la reserva
def calcular_total(reserva, precio_habitacion=100):
    dias = (reserva.fecha_salida - reserva.fecha_entrada).days
    return precio_habitacion * dias

# Función para registrar factura
def registrar_factura(cliente_var, reserva_var):
    cliente = cliente_var.get()
    reserva = reserva_var.get()

    if not cliente or not reserva:
        messagebox.showerror("Error", "Por favor, seleccione un cliente y una reserva.")
        return

    fecha_salida = datetime.now()  # Ejemplo de uso de fecha actual como fecha de salida
    generar_factura(cliente, reserva, fecha_salida)

# Crear interfaz de facturación
def crear_interfaz_facturacion():
    root = tk.Tk()
    root.title("Sistema de Facturación")

    frame_facturacion = tk.Frame(root)
    frame_facturacion.pack(padx=10, pady=10)

    tk.Label(frame_facturacion, text="Registro de Factura").grid(row=0, column=0, columnspan=2)

    # Cliente
    tk.Label(frame_facturacion, text="Cliente:").grid(row=1, column=0)
    cliente_var = tk.StringVar()
    entry_cliente = tk.Entry(frame_facturacion, textvariable=cliente_var)
    entry_cliente.grid(row=1, column=1)

    # Reserva
    tk.Label(frame_facturacion, text="Reserva:").grid(row=2, column=0)
    reserva_var = tk.StringVar()
    entry_reserva = tk.Entry(frame_facturacion, textvariable=reserva_var)
    entry_reserva.grid(row=2, column=1)

    # Botón para registrar factura
    btn_guardar_factura = tk.Button(frame_facturacion, text="Registrar Factura", command=lambda: registrar_factura(cliente_var, reserva_var))
    btn_guardar_factura.grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()

# Ejecutar la interfaz de facturación
if __name__ == "__main__":
    crear_interfaz_facturacion()

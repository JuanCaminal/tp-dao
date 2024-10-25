from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class Habitacion:
    def __init__(self, numero, tipo, estado, precio_por_noche):
        self.numero = numero
        self.tipo = tipo  # Puede ser 'simple', 'doble', o 'suite'
        self.estado = estado  # 'disponible' o 'ocupada'
        self.precio_por_noche = precio_por_noche
        self.fechas_ocupadas = []

    def agregar_reserva(self, fecha_entrada, fecha_salida):
        self.fechas_ocupadas.append((fecha_entrada, fecha_salida))

    def esta_disponible(self, fecha_entrada, fecha_salida):
        for fecha_reserva_entrada, fecha_reserva_salida in self.fechas_ocupadas:
            if (fecha_reserva_entrada <= fecha_salida and fecha_reserva_salida >= fecha_entrada):
                return False
        return True

    def __str__(self):
        return f'Habitación {self.numero} - Tipo: {self.tipo} - Estado: {self.estado} - Precio: {self.precio_por_noche} por noche'


class SistemaGestionHabitaciones:
    def __init__(self):
        self.habitaciones = []

    def registrar_habitacion(self, numero, tipo, estado, precio_por_noche):
        nueva_habitacion = Habitacion(numero, tipo, estado, precio_por_noche)
        self.habitaciones.append(nueva_habitacion)
        print(f"Habitación {numero} registrada exitosamente.")

    def consultar_disponibilidad(self, fecha_entrada, fecha_salida):
        habitaciones_disponibles = [habitacion for habitacion in self.habitaciones if habitacion.esta_disponible(fecha_entrada, fecha_salida)]
        return habitaciones_disponibles


class InterfazConsultaDisponibilidad:
    def __init__(self, root, sistema_gestion_habitaciones):
        self.root = root
        self.root.title("Consulta de Disponibilidad de Habitaciones")
        self.sistema_gestion_habitaciones = sistema_gestion_habitaciones

        # Etiquetas y campos de entrada para las fechas
        tk.Label(root, text="Fecha de Entrada (YYYY-MM-DD):").grid(row=0, column=0)
        self.entry_fecha_entrada = tk.Entry(root)
        self.entry_fecha_entrada.grid(row=0, column=1)

        tk.Label(root, text="Fecha de Salida (YYYY-MM-DD):").grid(row=1, column=0)
        self.entry_fecha_salida = tk.Entry(root)
        self.entry_fecha_salida.grid(row=1, column=1)

        # Botón para consultar disponibilidad
        tk.Button(root, text="Consultar Disponibilidad", command=self.consultar_disponibilidad).grid(row=2, column=0, columnspan=2)

        # Área de texto para mostrar habitaciones disponibles
        self.resultado = tk.Text(root, width=50, height=10, state='disabled')
        self.resultado.grid(row=3, column=0, columnspan=2)

    def consultar_disponibilidad(self):
        # Obtener las fechas ingresadas
        fecha_entrada_texto = self.entry_fecha_entrada.get()
        fecha_salida_texto = self.entry_fecha_salida.get()

        try:
            fecha_entrada = datetime.strptime(fecha_entrada_texto, "%Y-%m-%d").date()
            fecha_salida = datetime.strptime(fecha_salida_texto, "%Y-%m-%d").date()

            # Validar que la fecha de entrada sea anterior a la de salida
            if fecha_entrada >= fecha_salida:
                raise ValueError("La fecha de entrada debe ser anterior a la fecha de salida.")
        except ValueError as e:
            messagebox.showerror("Error", f"Formato de fecha incorrecto o fechas no válidas. {str(e)}")
            return

        # Consultar disponibilidad en el sistema de gestión de habitaciones
        habitaciones_disponibles = self.sistema_gestion_habitaciones.consultar_disponibilidad(fecha_entrada, fecha_salida)

        # Mostrar los resultados
        self.resultado.config(state='normal')
        self.resultado.delete(1.0, tk.END)

        if habitaciones_disponibles:
            for habitacion in habitaciones_disponibles:
                self.resultado.insert(tk.END, f"{habitacion}\n")
        else:
            self.resultado.insert(tk.END, "No hay habitaciones disponibles para estas fechas.")

        self.resultado.config(state='disabled')


# Ejemplo de uso
root = tk.Tk()
root.minsize(400, 300)
sistema_gestion_habitaciones = SistemaGestionHabitaciones()
sistema_gestion_habitaciones.registrar_habitacion(101, "doble", "disponible", 150.0)
sistema_gestion_habitaciones.registrar_habitacion(102, "suite", "disponible", 300.0)

# Agregamos algunas reservas para probar
sistema_gestion_habitaciones.habitaciones[0].agregar_reserva(datetime(2024, 10, 25).date(), datetime(2024, 10, 27).date())
sistema_gestion_habitaciones.habitaciones[1].agregar_reserva(datetime(2024, 10, 26).date(), datetime(2024, 10, 28).date())

InterfazConsultaDisponibilidad(root, sistema_gestion_habitaciones)
root.mainloop()

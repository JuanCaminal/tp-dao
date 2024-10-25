import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry

class PantallaOcupacion:
    def __init__(self, master, sistema_hotel):
        self.master = master
        self.master.title("Ocupación Promedio por Tipo de Habitación")
        
        self.sistema_hotel = sistema_hotel
        
        # Etiquetas y campos de entrada de fecha
        tk.Label(master, text="Fecha de inicio:").pack(pady=5)
        self.entry_fecha_inicio = DateEntry(master, width=12, background="darkblue", foreground="white", date_pattern="yyyy-MM-dd")
        self.entry_fecha_inicio.pack()

        tk.Label(master, text="Fecha de fin:").pack(pady=5)
        self.entry_fecha_fin = DateEntry(master, width=12, background="darkblue", foreground="white", date_pattern="yyyy-MM-dd")
        self.entry_fecha_fin.pack()

        # Botón para mostrar el reporte de ocupación promedio
        btn_mostrar_ocupacion = tk.Button(master, text="Mostrar Ocupación Promedio", command=self.mostrar_ocupacion_promedio)
        btn_mostrar_ocupacion.pack(pady=10)

        # Crear el Treeview para mostrar la ocupación
        self.columns = ("Tipo", "Ocupación")
        self.tree = ttk.Treeview(master, columns=self.columns, show="headings")
        self.tree.heading("Tipo", text="Tipo de Habitación")
        self.tree.heading("Ocupación", text="Ocupación Promedio")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

    def mostrar_ocupacion_promedio(self):
        try:
            fecha_inicio = datetime.strptime(self.entry_fecha_inicio.get(), "%Y-%m-%d")
            fecha_fin = datetime.strptime(self.entry_fecha_fin.get(), "%Y-%m-%d")
            ocupacion_promedio = self.sistema_hotel.ocupacion_promedio_por_tipo(fecha_inicio, fecha_fin)

            # Limpiar el árbol antes de agregar nuevos datos
            for i in self.tree.get_children():
                self.tree.delete(i)

            if ocupacion_promedio:
                for tipo, promedio in ocupacion_promedio.items():
                    self.tree.insert("", "end", values=(tipo, f"{promedio:.2%}"))
            else:
                messagebox.showinfo("Reporte de Ocupación Promedio", "No hay datos para mostrar.")
        except ValueError:
            messagebox.showerror("Error", "Por favor selecciona fechas válidas.")

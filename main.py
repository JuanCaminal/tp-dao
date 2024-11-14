import tkinter as tk
from db.db_connect import DBConnect
from pantallas.pantalla_principal import PantallaPrincipal  # Importa el menú principal
# from pantallas.reportes.pantalla_ocupa_promedio_tipo_hab_2 import PantallaOcupacion  # Importa la pantalla de ocupación


def main():
    db = DBConnect()

    menu = PantallaPrincipal(db)
    menu.mainloop()

    db.close_db()

if __name__ == '__main__':
    main()


#emif
# class SistemaHotel:
#     def __init__(self):
#         self.reservas = []
#         # Aquí puedes añadir más lógica para el sistema

# def mostrar_ocupacion_promedio():
#     nueva_ventana = tk.Toplevel(ventana)  # Crea una nueva ventana
#     PantallaOcupacion(nueva_ventana, sistema_hotel)  # Pasa el sistema_hotel a la nueva pantalla

# # Crear la ventana principal
# ventana = tk.Tk()
# ventana.title("Sistema de Gestión de Hotel")
# ventana.geometry("400x300")

# # Título de la ventana
# titulo = tk.Label(ventana, text="Bienvenido al Sistema de Gestión de Hotel", font=("Arial", 14))
# titulo.pack(pady=10)

# # Crear el sistema hotel
# sistema_hotel = SistemaHotel()

# # Botón para mostrar ocupación promedio
# btn_ocupacion = tk.Button(ventana, text="Ocupación Promedio", command=mostrar_ocupacion_promedio)
# btn_ocupacion.pack(pady=5)

# # Iniciar el bucle principal
# ventana.mainloop()
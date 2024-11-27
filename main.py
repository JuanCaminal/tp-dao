import tkinter as tk
from db.db_connect import DBConnect
from pantallas.pantalla_principal import PantallaPrincipal  # Importa el menú principal


def main():
    db = DBConnect()

    menu = PantallaPrincipal(db)
    menu.mainloop()

    db.close_db()


if __name__ == '__main__':
    main()

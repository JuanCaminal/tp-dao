import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5 import QtCore

# Nueva clase para la ventana de reportes
class ReportesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana de Reportes")
        self.setWindowIcon(QIcon("C:\\Users\\admin\\Downloads\\Unv\\recursos\\UTN_logo.ico"))

        label = QLabel("Esta es la ventana de reportes.", self)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setFont(QFont("Sans-serif", 16))

        layout = QVBoxLayout()
        layout.addWidget(label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


# Clase principal de la ventana
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UTN Hotel")
        self.setWindowIcon(QIcon("C:\\Users\\admin\\Downloads\\Unv\\recursos\\UTN_logo.ico"))

        # Crear un QLabel para la imagen de fondo
        background_label = QLabel(self)
        pixmap = QPixmap("C:\\Users\\admin\\Downloads\\Unv\\recursos\\fotor-20241113224158.jpg")
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        background_label.setGeometry(0, 0, 700, 500)

        # Título
        title = QLabel("MENU PRINCIPAL", self)
        title.setFont(QFont("Sans-serif", 18, QFont.Bold))
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("color: white;")  

        # Layout de botones (Grid)
        grid_layout = QGridLayout()

        # Crear botones con información correcta
        buttons_info = [
            ("Registrar \nHabitaciones", "C:\\Users\\admin\\Downloads\\Unv\\recursos\\cama-individual.png"),
            ("Registrar \nClientes", "C:\\Users\\admin\\Downloads\\Unv\\recursos\\personas.png"),
            ("Registrar \nReservas", "C:\\Users\\admin\\Downloads\\Unv\\recursos\\reserva.png"),
            ("Registrar \nFacturas", "C:\\Users\\admin\\Downloads\\Unv\\recursos\\cuenta.png"),
            ("  Asignar\nEmpleados\nHabitaciones", "C:\\Users\\admin\\Downloads\\Unv\\recursos\\desempleo.png"),
            ("Disponibilidad\nHabitaciones", "C:\\Users\\admin\\Downloads\\Unv\\recursos\\firmar.png"),
        ]

        row, col = 0, 0
        for name, icon_path in buttons_info:
            button = QPushButton(name)
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QtCore.QSize(30, 30))
            button.setFixedSize(125, 100)
            button.setFont(QFont("Sans-serif", 10))
            button.setStyleSheet("background-color: white; color: #333; border: 1px solid #DDD; padding: 8px;")

            grid_layout.addWidget(button, row, col)

            col += 1
            if col > 2:
                col = 0
                row += 1

        # Crear el botón "Reportes" y conectar con la ventana de reportes
        reportes_button = QPushButton("Reportes")
        reportes_button.setIcon(QIcon("C:\\Users\\admin\\Downloads\\Unv\\recursos\\reporte.png"))
        reportes_button.setIconSize(QtCore.QSize(30, 30))
        reportes_button.setFixedSize(125, 100)
        reportes_button.setFont(QFont("Sans-serif", 10))
        reportes_button.setStyleSheet("background-color: white; color: #333; border: 1px solid #DDD; padding: 8px;")

        # Colocar el botón "Reportes" en el centro de la última fila ocupando 3 columnas
        grid_layout.addWidget(reportes_button, row, 1, 1, 2)

        # Conectar el botón con la nueva ventana
        reportes_button.clicked.connect(self.open_reportes_window)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(grid_layout)

        container = QWidget()
        container.setLayout(main_layout)

        # Agregar el contenedor de botones sobre el fondo
        self.setCentralWidget(container)
        background_label.lower()

    def open_reportes_window(self):
        # Crear y mostrar la ventana de reportes
        self.reportes_window = ReportesWindow()
        self.reportes_window.show()

# Ejecución de la aplicación
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setFixedSize(700, 500)
    window.show()

    app.exec_()

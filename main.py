import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5 import QtCore
from reportes import ReportesWindow  


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UTN Hotel")
        self.setWindowIcon(QIcon("C:\\Users\\admin\\Downloads\\Unv\\recursos\\UTN_logo.ico"))

        background_label = QLabel(self)
        pixmap = QPixmap("C:\\Users\\admin\\Downloads\\Unv\\recursos\\fotor-20241113224158.jpg")
        background_label.setPixmap(pixmap)
        background_label.setScaledContents(True)
        background_label.setGeometry(0, 0, 700, 500)

        title = QLabel("MENU PRINCIPAL", self)
        title.setFont(QFont("Sans-serif", 18, QFont.Bold))
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("color: white;")  

        reportes_button = QPushButton("Reportes")

        reportes_button.clicked.connect(self.open_reportes_window)


        grid_layout = QGridLayout()

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

        reportes_button = QPushButton("Reportes")
        reportes_button.setIcon(QIcon("C:\\Users\\admin\\Downloads\\Unv\\recursos\\reporte.png"))
        reportes_button.setIconSize(QtCore.QSize(30, 30))
        reportes_button.setFixedSize(125, 100)
        reportes_button.setFont(QFont("Sans-serif", 10))
        reportes_button.setStyleSheet("background-color: white; color: #333; border: 1px solid #DDD; padding: 8px;")

        grid_layout.addWidget(reportes_button, row, 1, 1, 2)

        reportes_button.clicked.connect(self.open_reportes_window)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(grid_layout)

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)
        background_label.lower()
                
    def open_reportes_window(self):
        # Crear y mostrar la ventana de reportes
        self.reportes_window = ReportesWindow()
        self.reportes_window.show()
        
        
        




if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setFixedSize(700, 600)
    window.show()

    app.exec_()

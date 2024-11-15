import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from PIL import Image, ImageTk
from reportes import ReportesWindow


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UTN Hotel")
        self.geometry("1100x700")
        self.resizable(False, False)  
        self.iconbitmap("C:\\Users\\admin\\Downloads\\Unv\\recursos\\UTN_logo.ico")

        bg_image = Image.open("C:\\Users\\admin\\Downloads\\Unv\\tp-dao\\recursos\\fotor-20241115194144.jpg")
        bg_image = bg_image.resize((1100, 700), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        background_label = tk.Label(self, image=self.bg_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        
  

        buttons_info = [
            ("Registrar \nHabitaciones", "C:\\Users\\admin\\Downloads\\Unv\\tp-dao\\recursos\\habitacion.png"),
            ("Registrar \nClientes", "C:\\Users\\admin\\Downloads\\Unv\\recursos\\personas.png"),
            ("Registrar \nReservas", "C:\\Users\\admin\\Downloads\\Unv\\tp-dao\\recursos\\reserva.png"),
            ("Registrar \nFacturas", "C:\\Users\\admin\\Downloads\\Unv\\tp-dao\\recursos\\factura.png"),
            ("  Asignar\nEmpleados\nHabitaciones", "C:\\Users\\admin\\Downloads\\Unv\\recursos\\desempleo.png"),
            ("Disponibilidad\nHabitaciones", "C:\\Users\\admin\\Downloads\\Unv\\recursos\\firmar.png"),
        ]

        grid_frame = tk.Frame(self, bg="#18171c")  
        grid_frame.pack(expand=True, pady=10)

        row, col = 0, 0
        for name, icon_path in buttons_info:
            icon_image = Image.open(icon_path).resize((40, 40), Image.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_image)

            button = tk.Button(
                grid_frame,
                text=name,
                image=icon_photo,
                compound="top",
                font=Font(family="Sans-serif", size=11),
                bg="#282828", 
                activebackground="#444444", 
                activeforeground="white", 
                fg="white",
                bd=0,  
                width=170,
                height=150,
                command=lambda n=name: self.button_clicked(n)
            )
            button.image = icon_photo  
            button.grid(row=row, column=col, padx=10, pady=10)

            col += 1
            if col > 2:
                col = 0
                row += 1

        report_icon = Image.open("C:\\Users\\admin\\Downloads\\Unv\\tp-dao\\recursos\\dinero.png").resize((40, 40), Image.LANCZOS)
        report_photo = ImageTk.PhotoImage(report_icon)

        reportes_button = tk.Button(
            grid_frame,
            text="Reportes",
            image=report_photo,
            compound="top",
            font=Font(family="Sans-serif", size=11),
            bg="#282828",  
            fg="white", 
            activebackground="#444444", 
            activeforeground="white",  
            bd=0,  
            width=170,
            height=150,
            command=self.open_reportes_window
        )
        reportes_button.image = report_photo
        reportes_button.grid(row=row + 1, column=1, columnspan=1, pady=20)  

    def button_clicked(self, name):
        print(f"Botón '{name}' presionado")

    def open_reportes_window(self):
        reportes_window = ReportesWindow()
        reportes_window.show()

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()

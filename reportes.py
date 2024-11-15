import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

class ReportesWindow(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Reportes")
        self.geometry("800x600")
        self.resizable(False, False)  
        self.configure(bg="#332f2C")  
        self.iconbitmap("C:\\Users\\admin\\Downloads\\Unv\\recursos\\UTN_logo.ico")

        
        self.center_window(800, 600)

        title_font = Font(family="Sans-serif", size=14, weight="bold")
        title_label = tk.Label(
            self, 
            text="Reportes", 
            font=title_font, 
            fg="white", 
            bg="#1414b8", 
            pady=10
        )
        title_label.pack(fill=tk.X, pady=(20, 10))

        button_frame = tk.Frame(self, bg="#332f2C")
        button_frame.pack(expand=True)

        buttons_info = [
            "Reservas Realizadas en un periodo de tiempo",
            "Reporte ingresos por habitaciones y servicios extras",
            "Reporte de ocupación promedio por tipo de habitación"
        ]

        button_font = Font(family="Sans-serif", size=10)
        for text in buttons_info:
            button = tk.Button(
                button_frame, 
                text=text, 
                font=button_font, 
                bg="#1414b8", 
                fg="white", 
                activebackground="#1a1aff", 
                activeforeground="white",
                width=50, 
                height=2, 
                relief="flat",
                command=lambda t=text: self.button_clicked(t)
            )
            button.pack(pady=10)  

    def button_clicked(self, text):
        print(f"Botón '{text}' presionado")

    def center_window(self, width, height):
        """Centrar la ventana en la pantalla."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() 
    window = ReportesWindow()
    window.mainloop()

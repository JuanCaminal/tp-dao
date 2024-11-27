class WindowSizeHelper:
    @staticmethod
    def centrar_ventana(window):
        # Obtener el tamaño actual de la ventana
        window_width = window.winfo_width()
        window_height = window.winfo_height()

        # Obtener las dimensiones de la pantalla
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calcular la posición para centrar la ventana
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)

        # Establecer la nueva geometría de la ventana
        window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    @staticmethod
    def set_size(window, width, height):
        window.geometry(f"{width}x{height}")


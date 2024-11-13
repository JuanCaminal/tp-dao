class Habitacion:
    def __init__(self, numero, tipo, estado, precio_por_noche): 
        self._numero = numero
        self._tipo = tipo  # Puede ser 'simple', 'doble', o 'suite'
        self._estado = estado  # 'disponible' o 'ocupada'
        self._precio_por_noche = precio_por_noche
    
    def __str__(self):  # se ejecuta cuando se trata de convertir al objeto en string
        # return f"{self.numero} from {self.house}"
        ...
    
    # Getters y Setters
    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, numero):
        self._numero = numero

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, tipo):
        self._tipo = tipo

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, estado):
        self._estado = estado
    
    @property
    def precio_por_noche(self):
        return self._precio_por_noche

    @precio_por_noche.setter
    def precio_por_noche(self, precio):
        self._precio_por_noche = precio
        
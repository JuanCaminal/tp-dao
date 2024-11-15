from datetime import datetime

from clases.habitacion import Habitacion
from repositories.habitacion_repository import HabitacionRepository

class HabitacionService:
    def __init__(self, db):
        self.habitacion_repository = HabitacionRepository(db)

    def get_all(self):
        return self.habitacion_repository.get_all()

    def get_by_id(self, numero):
        return self.habitacion_repository.get_by_id(numero)

    def create(self, habitacion):
        habitacion = Habitacion(
            numero=habitacion['numero'],
            tipo=habitacion['tipo'],
            estado=habitacion['estado'],
            precio_por_noche=habitacion['precio']
        )
        return self.habitacion_repository.create(habitacion)

    def update(self, numero, habitacion):
        return self.habitacion_repository.update(numero, habitacion)

    def delete(self, numero):
        return self.habitacion_repository.delete(numero)

    def get_habitaciones_disponibles_by_date_range(self, fecha_inicio, fecha_fin):
        # Convertir las fechas a formato yyyy-mm-dd
        fecha_entrada = self.convertir_fecha_dd_mm_aaaa_a_yyyy_mm_dd(fecha_inicio.strftime("%d/%m/%Y"))
        fecha_salida = self.convertir_fecha_dd_mm_aaaa_a_yyyy_mm_dd(fecha_fin.strftime("%d/%m/%Y"))

        return self.habitacion_repository.get_diponibles_by_date_range(fecha_entrada, fecha_salida)

    @staticmethod
    def convertir_fecha_dd_mm_aaaa_a_yyyy_mm_dd(fecha):
        return datetime.strptime(fecha, '%d/%m/%Y').strftime('%Y-%m-%d')
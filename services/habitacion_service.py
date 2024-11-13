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

from clases.reserva import Reserva
from repositories.reserva_repository import ReservaRepository

class ReservaService:
    def __init__(self, db):
        self.reserva_repository = ReservaRepository(db)

    def get_all(self):
        return self.reserva_repository.get_all()

    def get_by_id(self, id):
        return self.reserva_repository.get_by_id(id)

    def create(self, reserva):
        reserva = Reserva(
            cliente=reserva['cliente'],
            habitacion=reserva['habitacion'],
            fecha_entrada=reserva['fecha_entrada'],
            fecha_salida=reserva['fecha_salida'],
            cantidad_personas=reserva['cantidad_personas']
        )
        return self.reserva_repository.create(reserva)

    def update(self, id, reserva):
        return self.reserva_repository.update(id, reserva)

    def delete(self, id):
        return self.reserva_repository.delete(id)
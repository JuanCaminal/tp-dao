from clases.reserva import Reserva
from repositories.reserva_repository import ReservaRepository
from services.habitacion_service import HabitacionService


class ReservaService:
    def __init__(self, db):
        self.reserva_repository = ReservaRepository(db)
        self.habitacion_service = HabitacionService(db)

    def get_all(self):
        return self.reserva_repository.get_all()

    def get_by_id(self, id):
        return self.reserva_repository.get_by_id(id)

    def get_reservas_by_date_range(self, fecha_inicio, fecha_fin):
        return self.reserva_repository.get_by_date_range(fecha_inicio, fecha_fin)

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

from repositories.cliente_repository import ClienteRepository
from clases.cliente import Cliente


class ClienteService:
    def __init__(self, db):
        self.cliente_repository = ClienteRepository(db)

    def get_all(self):
        return self.cliente_repository.get_all()

    def get_by_id(self, id):
        return self.cliente_repository.get_by_id(id)

    def create(self, cliente_data):
        cliente = Cliente(
            nombre=cliente_data["nombre"],
            apellido=cliente_data["apellido"],
            direccion=cliente_data["direccion"],
            telefono=cliente_data["telefono"],
            email=cliente_data["email"],
            nro_documento=cliente_data["nro_documento"]  # Asegúrate de pasar el nro_documento
        )
        return self.cliente_repository.create(cliente)

    def update(self, id, cliente_data):
        return self.cliente_repository.update(id, cliente_data)

    def delete(self, id):
        return self.cliente_repository.delete(id)

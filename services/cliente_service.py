from repositories.cliente_repository import ClienteRepository
from clases.cliente import Cliente


class ClienteService:
    def __init__(self, db):
        self.cliente_repository = ClienteRepository(db)

    def get_all(self):
        return self.cliente_repository.get_all()

    def get_by_id(self, id):
        return self.cliente_repository.get_by_id(id)

    def create(self, cliente):
        cliente = Cliente(
            nombre=cliente['nombre'],
            apellido=cliente['apellido'],
            direccion=cliente['direccion'],
            telefono=cliente['telefono'],
            email=cliente['email']
        )
        return self.cliente_repository.create(cliente)

    def update(self, id, cliente):
        return self.cliente_repository.update(id, cliente)

    def delete(self, id):
        return self.cliente_repository.delete(id)
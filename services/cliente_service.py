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
            nro_documento=cliente_data["nro_documento"],
            puntos_fidelizacion=0
        )
        return self.cliente_repository.create(cliente)

    def update(self, id, cliente_data):
        # Aquí debemos crear el objeto Cliente para pasar a la capa de repositorio
        cliente = Cliente(
            id_cliente=id,
            nombre=cliente_data["nombre"],
            apellido=cliente_data["apellido"],
            direccion=cliente_data["direccion"],
            telefono=cliente_data["telefono"],
            email=cliente_data["email"],
            nro_documento=cliente_data["nro_documento"],
            puntos_fidelizacion=cliente_data["puntos_fidelizacion"]
        )
        return self.cliente_repository.update(id, cliente)

    def delete(self, id):
        return self.cliente_repository.delete(id)

    def acumular_puntos(self, id_cliente, puntos):
        puntos_actuales = self.cliente_repository.get_puntos(id_cliente)
        nuevos_puntos = puntos_actuales + puntos
        self.cliente_repository.actualizar_puntos(id_cliente, nuevos_puntos)
        return nuevos_puntos

    def canjear_puntos(self, id_cliente, puntos_a_canjear):
        puntos_actuales = self.cliente_repository.get_puntos(id_cliente)
        if puntos_actuales >= puntos_a_canjear:
            nuevos_puntos = puntos_actuales - puntos_a_canjear
            self.cliente_repository.actualizar_puntos(id_cliente, nuevos_puntos)
            return nuevos_puntos
        else:
            raise ValueError("Puntos insuficientes para canjear.")

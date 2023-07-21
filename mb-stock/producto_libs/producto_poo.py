class Producto:
    """
    Clase Producto
    """

    def __init__(self, id, descripcion, proveedor, precio):
        self.id = id
        self.descripcion = descripcion
        self.proveedor = proveedor
        self.precio = precio

    def __repr__(self):
        return f"{self.id} {self.descripcion} {self.proveedor} {self.precio}"

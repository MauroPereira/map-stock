from producto_libs.producto_poo import Producto
from producto_libs.adv_libs.peewee_mod import PeeweeDb
from producto_libs.adv_libs.decorator_mod import decorador_deprecrated


class CrudSqlite3:
    def __init__(self):
        try:
            self.peewee_db = PeeweeDb()
        except Exception as err:
            print(f"Error conectando a la base de datos: {err}")

    @decorador_deprecrated
    def get_connection(self, path="./database/bd.db", bd="sqlite3"):
        """
        Establece la conexion con la base de datos
        """
        pass

    @decorador_deprecrated
    def create_database(self):
        """
        Crea la/s tabla/s si no existen
        """
        pass

    def productos_get_list(self, filter=""):
        """
        Devuelve los valores de la base de datos como una lista de Productos
        """

        try:
            lista_productos = []

            lista_consultada = self.peewee_db.consulta()

            # Crea una lista de instancias de producto, con sus campos
            # rellenados con los datos de la BD
            for item in lista_consultada:
                if len(item) == 4:  # debido al ultimo item
                    producto = Producto(
                        id=item[0],
                        descripcion=item[1],
                        proveedor=item[2],
                        precio=item[3],
                    )
                    lista_productos.append(producto)

            return lista_productos

        except Exception as err:
            print(f"Error en productos_get_list: {err}")

    def producto_get_by_id(self, id):
        """
        Funcion que devuelve una instancia de la clase producto a partir del
        id o devuelve None
        """
        try:
            # Instancia de producto, donde sus campos son rellenados con los
            # datos de la BD
            item = self.peewee_db.consulta_por_id(id)

            if item:
                producto = Producto(
                    id=item[0][0],
                    descripcion=item[0][1],
                    proveedor=item[0][2],
                    precio=item[0][3],
                )
                return producto
            else:
                return None

        except Exception as err:
            print(f"Error en producto_get_by_id: {err}")
            return None

    def producto_add(self, producto):
        """
        Agrega un Producto a la base de datos
        """
        try:
            self.peewee_db.alta(
                (producto.descripcion, producto.proveedor, producto.precio)
            )
            return True
        except Exception as err:
            print(f"Error en producto_add: {err}")
            return False

    def producto_update(self, producto):
        """
        Actualiza los valores de un Producto seleccionado en la base de datos
        """
        try:
            self.peewee_db.modifica(
                (
                    producto.id,
                    producto.descripcion,
                    producto.proveedor,
                    producto.precio,
                )
            )
            return True

        except Exception as err:
            print(f"Error en producto_update: {err}")
            return False

    def producto_delete(self, producto):
        """
        Borra un Producto seleccionado de la base de datos
        """
        try:
            self.peewee_db.baja(producto.id)
            return True

        except Exception as err:
            print(f"Error en producto_delete: {err}")
            return False


if __name__ == "__main__":
    print("Fin")

import os
import sys
import subprocess
import threading
from pathlib import Path
from producto_libs.crud_poo import CrudSqlite3
from producto_libs.regex import Regex

# from producto_libs.producto_poo import Producto


class Model(CrudSqlite3):
    def __init__(self):
        super().__init__()

    def chequear_selected_id(self, selected_id):
        """
        Chequea si se pudo borrar el id seleccionado
        """

        if selected_id:
            # pedir confirmacion
            producto = self.producto_get_by_id(selected_id)
            print("producto:" + str(producto))
            if producto != None:
                self.producto_delete(producto)
                return "delete_ok"
            else:
                return "delete_nok"
        else:
            return "no_selected_product"

    def chequear_agregar_producto(self, producto):
        """
        Chequea si se pudo agregar el producto
        """
        if Regex.comprueba_descripcion(producto.descripcion) == False:
            raise Exception("Error de regex en el campo descripcion")
        elif Regex.comprueba_precio(producto.precio) == False:
            raise Exception("Error de regex en el campo precio")
        elif Regex.comprueba_proveedor(producto.proveedor) == False:
            raise Exception("Error de regex en el campo proveedor")
        else:
            return self.producto_add(producto)

    def chequear_actualizar_producto(self, producto):
        """
        Chequea si se pudo actualizar el producto
        """
        if not Regex.comprueba_descripcion(producto.descripcion):
            raise Exception("Error de regex en el campo descripcion")
        elif not Regex.comprueba_precio(producto.precio):
            raise Exception("Error de regex en el campo precio")
        elif not Regex.comprueba_proveedor(producto.proveedor):
            raise Exception("Error de regex en el campo proveedor")
        else:
            return self.producto_update(producto)

    def pedir_todos_productos(self):
        """
        Devuelve una lista de todos los objetos productos
        """
        return self.productos_get_list()

    def llenar_tree_view(self, treeview):
        """
        Carga los valores en el tree view
        """

        for producto in self.pedir_todos_productos():
            print(producto)

        for producto in self.pedir_todos_productos():
            values = (
                producto.descripcion,
                producto.proveedor,
                producto.precio,
            )
            treeview.insert("", 0, text=producto.id, values=values)

    def salir(self):
        """
        Realiza todo lo necesario para un correcto cierre del programa
        """


if __name__ == "__main__":
    model = Model()

    # Tests de funcionamiento de clase:

    # Alta
    # producto = Producto(id=0,descripcion='prueba',proveedor='proveedor prueba',precio=100)
    # print(model.producto_add(producto))

    # Modificacion
    producto = model.producto_get_by_id(7)
    if producto:
        producto.descripcion = "Producto 8"
        model.producto_update(producto)
    else:
        print("Producto no existe")

    # Delete
    # model.producto_delete(producto)

    print("*" * 50)

    # listado

    for item in model.productos_get_list():
        print(item)

    # filtrado
    print("*" * 50, "Filtrado")
    for item in model.productos_get_list("descripcion LIKE 'Pro%'"):
        print(item)

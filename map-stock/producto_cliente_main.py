# ##########################################################################################
#
# PROGRAMA: GESTIÓN DE PRODUCTOS - CLIENTE
# NOMBRE CLAVE DEL PROYECTO: MB-STOCK
#
# Desarrolladores:
#   • Mauro Alejandro Pereira <mauro.a.pereira@gmail.com>
#
# ##########################################################################################

from producto_libs.comm_cliente_mod import CommCliente
from producto_libs.common_libs.char_cons_crud import CREATE_CHAR
from producto_libs.common_libs.char_cons_crud import UPDATE_CHAR
from producto_libs.common_libs.char_cons_crud import READ_ID_CHAR
from producto_libs.common_libs.char_cons_crud import DELETE_CHAR
from producto_libs.common_libs.char_cons_crud import OKD_CHAR
from producto_libs.common_libs.convert_data_types import (
    convert_bytes_array_to_list,
)
from producto_libs.common_libs.client_functions import check_received


class Empaquetar:
    """
    Clase que se encarga de preparar la información para enviarsela al servidor
    """

    def __init__(self):
        self.comm_cliente = CommCliente()

    def agregar_producto(
        self,
        descripction="Tomate",
        proveedor="Pepito",
        precio="10.5",
    ):
        """
        Agrega un producto desde cliente
        """
        print(
            "Se va a empaquetar:\nDescripción: {0}\nProveedor: {1}\nPrecio: {2} \n".format(
                descripction, proveedor, precio
            )
        )

        self.comm_cliente.load_data_int(CREATE_CHAR)  # indica agregado
        self.comm_cliente.load_data_str(descripction)
        self.comm_cliente.load_data_str(proveedor)
        self.comm_cliente.load_data_str(precio)

        self.comm_cliente.send_and_receive_data()
        self.comm_cliente.print_received_data()

        final_list_received = convert_bytes_array_to_list(
            self.comm_cliente.value_received
        )
        check_received(final_list_received[0], "Producto agregado con éxito")

        self.comm_cliente.erase_sent_and_received_data()

    def eliminar_producto(self, id="1"):
        """
        Elimina un producto por ID desde cliente
        """

        self.comm_cliente.load_data_int(DELETE_CHAR)
        self.comm_cliente.load_data_str(
            str(id)
        )  # importante: convertir en string

        self.comm_cliente.send_and_receive_data()
        self.comm_cliente.print_received_data()

        final_list_received = convert_bytes_array_to_list(
            self.comm_cliente.value_received
        )
        check_received(
            final_list_received[0], "\nProducto eliminado con éxito"
        )

        self.comm_cliente.erase_sent_and_received_data()

    def consultar_producto_id(self, id="1"):
        """
        Consulta un producto por ID desde cliente
        """

        self.comm_cliente.load_data_int(READ_ID_CHAR)
        self.comm_cliente.load_data_str(
            str(id)
        )  # importante: convertir en string

        self.comm_cliente.send_and_receive_data()
        self.comm_cliente.print_received_data()

        final_list_received = convert_bytes_array_to_list(
            self.comm_cliente.value_received
        )
        check_received(
            final_list_received[0], "\nProducto consultado con éxito"
        )
        if final_list_received[0] == chr(OKD_CHAR):
            print("\nID\tDescripción\tProveedor\tPrecio")
            for val in final_list_received[1:]:
                print(val, end="\t")
            print("")

        self.comm_cliente.erase_sent_and_received_data()

    def modificar_producto(
        self,
        id=2,
        descripction="Pera",
        proveedor="Juancito",
        precio="8.8",
    ):
        """
        Modifica un producto desde cliente
        """
        print(
            "Se va a empaquetar:\nID: {0}\nDescripción: {1}\nProveedor: {2}\nPrecio: {3} \n".format(
                str(id), descripction, proveedor, precio
            )
        )

        self.comm_cliente.load_data_int(UPDATE_CHAR)  # indica modificación
        self.comm_cliente.load_data_str(
            str(id)
        )  # importante: convertir en string
        self.comm_cliente.load_data_str(descripction)
        self.comm_cliente.load_data_str(proveedor)
        self.comm_cliente.load_data_str(precio)

        self.comm_cliente.send_and_receive_data()
        self.comm_cliente.print_received_data()

        final_list_received = convert_bytes_array_to_list(
            self.comm_cliente.value_received
        )
        check_received(
            final_list_received[0], "\nProducto modificado con éxito"
        )

        self.comm_cliente.erase_sent_and_received_data()

    def salir_cliente_producto(self):
        """
        Se encarga de salir del programa
        """
        print("Saliendo del programa...")
        self.comm_cliente.close_conection()


if __name__ == "__main__":

    opcion_repeat = True
    bucle_principal = True

    while bucle_principal:
        empaquetar = Empaquetar()  # Inicia la conexion con el servidor

        while opcion_repeat:
            print(
                "\nOperaciones:\n"
                + "1 - Agregar Producto\n"
                + "2 - Consultar un Producto\n"
                + "3 - Consultar lista completa de Producto\n"
                + "4 - Eliminar Producto\n"
                + "5 - Modificar Producto\n"
                + "0 - Salir\n"
            )
            opcion = int(input("Ingrese una opción: "))
            if not (opcion > -1 and opcion < 6):
                print("Error: Opción no valida")
            else:
                opcion_repeat = False
            print(30 * "*")

        if opcion == 1:
            descripcion = input(
                "Ingrese una descripción de producto sin espacios: "
            )
            proveedor = input("Ingrese proveedor del producto sin espacios: ")

            precio = str(
                input("Ingrese el precio del producto con decimales: ")
            )
            empaquetar.agregar_producto(descripcion, proveedor, precio)
            empaquetar.salir_cliente_producto()
            opcion_repeat = True

        elif opcion == 2:
            id = int(input("Ingrese la ID de producto a consultar: "))
            empaquetar.consultar_producto_id(id)
            empaquetar.salir_cliente_producto()
            opcion_repeat = True

        elif opcion == 3:
            print("Función todavía no implementada\n")
            empaquetar.salir_cliente_producto()
            opcion_repeat = True

        elif opcion == 4:
            id = int(input("Ingrese la ID del Producto a eliminar: "))
            empaquetar.eliminar_producto(id)
            empaquetar.salir_cliente_producto()
            opcion_repeat = True

        elif opcion == 5:
            id = int(input("Ingrese la ID de producto a modificar: "))
            descripcion = input(
                "Ingrese la nueva descripción de producto sin espacios: "
            )
            proveedor = input(
                "Ingrese el nuevo proveedor del producto sin espacios: "
            )
            precio = str(
                input("Ingrese el nuevo precio del producto con decimales: ")
            )
            empaquetar.modificar_producto(id, descripcion, proveedor, precio)
            empaquetar.salir_cliente_producto()
            opcion_repeat = True

        else:
            empaquetar.salir_cliente_producto()
            bucle_principal = False
    print("Fin")

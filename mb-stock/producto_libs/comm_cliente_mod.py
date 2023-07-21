import socket
import binascii

print("Name in comm_servidor_mod.py:" + str(__name__))

if __name__ == "__main__":
    from common_libs.char_cons_crud import CREATE_CHAR
    from common_libs.char_cons_crud import READ_ID_CHAR
    from common_libs.char_cons_crud import READ_LST_CHAR
    from common_libs.char_cons_crud import UPDATE_CHAR
    from common_libs.char_cons_crud import DELETE_CHAR
    from common_libs.char_cons_crud import OK_CHAR
    from common_libs.char_cons_crud import OKD_CHAR
    from common_libs.char_cons_crud import NOK_CHAR
    from common_libs.convert_data_types import char_to_bytes
    from common_libs.convert_data_types import convert_bytearrays_to_str

elif __name__ == "producto_libs.comm_cliente_mod":
    from producto_libs.common_libs.char_cons_crud import CREATE_CHAR
    from producto_libs.common_libs.char_cons_crud import READ_ID_CHAR
    from producto_libs.common_libs.char_cons_crud import READ_LST_CHAR
    from producto_libs.common_libs.char_cons_crud import UPDATE_CHAR
    from producto_libs.common_libs.char_cons_crud import DELETE_CHAR
    from producto_libs.common_libs.char_cons_crud import OK_CHAR
    from producto_libs.common_libs.char_cons_crud import OKD_CHAR
    from producto_libs.common_libs.char_cons_crud import NOK_CHAR
    from producto_libs.common_libs.convert_data_types import char_to_bytes
    from producto_libs.common_libs.convert_data_types import (
        convert_bytearrays_to_str,
    )


class CommCliente:
    """
    Clase que se encarga de abrir un nodo cliente y traficar información
    en bytes a otro nodo servidor
    """

    def __init__(self, debug_status: "Habilita el debug" = False):
        """
        Inicializa el nodo
        """
        self.debug_status = debug_status
        if self.debug_status:
            print("Modo DEBUG")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()  # dirección ip del servidor.
        self.port = 9999
        self.message = bytearray()
        self.value_received = bytearray()

        try:
            self.sock.connect((self.host, self.port))
        except ConnectionRefusedError as error:
            print("El servidor no está corriendo. {0}".format(error))
            exit()
        except Exception as e:
            print("Error desconocido. {0}".format(e))
            exit()

        print("Comunicación con el servidor establecida.")

    def load_data_int(
        self,
        int_to_send: "Valor entero a enviar" = 0x41,
        lf_enable: "Establece o no al final un LF" = True,
    ):
        """
        Carga el valor de un entero al bytearray a enviar
        """
        if self.debug_status:
            print(
                "Tipo y valor a enviar: "
                + str(type(int_to_send))
                + ", "
                + hex(int_to_send)
            )

        self.message += int_to_send.to_bytes(2, "big")
        if lf_enable:
            self.message += (0x09).to_bytes(2, "big")

        if self.debug_status:
            print("Mensaje a enviar: " + str(self.message))

            print(
                "Mensaje equivalente tipo string en hexadecimal: "
                + str(self.message.hex())
            )

    def load_data_str(self, str_to_send: "String a enviar" = "Tomate"):
        """
        Carga el valor de un string al bytearray a enviar
        """
        str_to_send += "\t"  # Necesario para separar los string de los demás datos a enviar

        if self.debug_status:
            print(
                "String a enviar: "
                + str(type(str_to_send))
                + ", "
                + str(str_to_send)
            )

        list_to_send = list(str_to_send)
        if self.debug_status:
            print("Pasado a lista: " + str(list_to_send))

        for letter in list_to_send:
            self.load_data_int(ord(letter), False)

    def send_and_receive_data(self):
        """
        Envia el valor precargado y recibe uno, el cual guarda
        """

        if self.debug_status is False:
            print("\nMensaje a enviar: " + str(self.message))

            print(
                "Mensaje equivalente tipo string en hexadecimal: "
                + str(self.message.hex())
            )

        self.sock.send(self.message)
        self.value_received += self.sock.recv(2046)

    def print_received_data(self):
        """
        Imprime los datos enviados y recibidos.
        """

        print(
            "\nMensaje recibido en hexadecimal del servidor: {0}".format(
                binascii.hexlify(self.value_received).decode("utf-8")
            )
        )
        print(
            "Mensaje tipo string del servidor: "
            + (self.value_received).decode("utf-8")
        )

    def check_received_data(self):
        """
        Chequea el estado del mensaje recibido
        """
        if convert_bytearrays_to_str(
            self.value_received
        ) == convert_bytearrays_to_str(char_to_bytes(OK_CHAR)):
            print("Operación exitosa")
        else:
            print("Error de operación")

    def erase_sent_and_received_data(self):
        """
        Borra los bytearray enviado y recibido.
        """

        self.message = bytearray()
        self.value_received = bytearray()

    def close_conection(self):
        """
        Se encarga de cerrar la conexión
        """
        self.sock.close()


if __name__ == "__main__":

    envio_producto = CommCliente()

    """
    # Carga de producto
    envio_producto.load_data_int(CREATE_CHAR)
    envio_producto.load_data_str("Tomate")
    envio_producto.load_data_str("Vanesa")
    envio_producto.load_data_str("10.22")
    envio_producto.send_and_receive_data()
    envio_producto.print_received_data()
    envio_producto.check_received_data()
    envio_producto.erase_sent_and_received_data()
    """

    # Se pide información de un producto en específicoq
    envio_producto.load_data_int(READ_ID_CHAR)  # "<"
    envio_producto.load_data_str("50")  # ID 3
    envio_producto.send_and_receive_data()
    envio_producto.print_received_data()
    envio_producto.check_received_data()
    envio_producto.erase_sent_and_received_data()

    envio_producto.close_conection()

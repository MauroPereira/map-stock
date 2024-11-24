import socket
import errno
import time
from yaspin import yaspin
from common_libs.print_colors import bcolors
from common_libs.keyboard_pressed import key_pressed
from common_libs.char_cons_crud import CREATE_CHAR
from common_libs.char_cons_crud import READ_ID_CHAR
from common_libs.char_cons_crud import READ_LST_CHAR
from common_libs.char_cons_crud import UPDATE_CHAR
from common_libs.char_cons_crud import DELETE_CHAR
from common_libs.char_cons_crud import NOK_CHAR
from common_libs.convert_data_types import convert_list_of_lists_to_simple_list
from common_libs.print_colors import print_colour


spinner = yaspin(text="Intentando conectar... presione q para salir.")

print("Name in comm_servidor_mod.py:" + str(__name__))

if __name__ == "__main__":
    from adv_libs.peewee_mod import PeeweeDb


class Desempaquetar:
    """
    Se encarga de desempaquetar la informacion del bytearray
    """

    def __init__(
        self,
        bytearray_a_analizar: "bytearray entrante" = "b'\x00e\x00",
        debug_status: "Debug" = False,
    ):
        self.peewee_db = PeeweeDb()

        self.bytearray_a_analizar = bytearray_a_analizar
        self.debug_status = debug_status

    def decodificar(self):
        """
        Convierte el bytearray a analizar en una lista
        """

        self.bytearray_a_analizar += bytearray("\t", "utf-8")
        print("\nRecibido compensado: " + str(self.bytearray_a_analizar))

        mensaje_bytearray = self.bytearray_a_analizar[1::2]

        mensaje_lst = []
        for byte_element in mensaje_bytearray:
            mensaje_lst.append(chr(byte_element))
        mensaje_str = "".join(mensaje_lst)

        self.mensaje_separado_lst = mensaje_str.split("\t")[:-1]

        if self.debug_status:
            print("Recibido: " + str(self.bytearray_a_analizar))
            print("Mensaje en bytearray: " + str(mensaje_bytearray))
            print("Mensaje tipo string: " + mensaje_str)
            print(
                "Mensaje tipo lista separado: "
                + str(self.mensaje_separado_lst)
            )

        print(21 * "*" + "\n" + "Mensaje decodificado:")
        for element in self.mensaje_separado_lst:
            print(element)
        print(21 * "*")

        # Chequea si el mensaje está vacío
        if len(self.mensaje_separado_lst) == 0:
            return "empty"
        return

    def operaciones_crud(self):
        """
        Gestiona las operaciones crud
        """
        status_lst = []

        if self.mensaje_separado_lst[0] == chr(CREATE_CHAR):  # ">"
            print("Elegido Alta de Producto")
            return_lst = []
            return_lst = self.peewee_db.alta(
                (
                    self.mensaje_separado_lst[1],
                    self.mensaje_separado_lst[2],
                    float(self.mensaje_separado_lst[3]),
                )
            )
            print("Listo Alta de Producto")
            status_lst += (
                return_lst  # adiciona a la lista status lo que devuelve crud
            )

        elif self.mensaje_separado_lst[0] == chr(DELETE_CHAR):  # "µ"
            print("Elegido Baja de Producto")
            return_lst = []
            return_lst = self.peewee_db.baja((self.mensaje_separado_lst[1]))
            print("Listo Baja de Producto")
            status_lst += (
                return_lst  # adiciona a la lista status lo que devuelve crud
            )

        elif self.mensaje_separado_lst[0] == chr(READ_ID_CHAR):  # "<"
            print("Elegido Consulta por ID de Producto")
            return_lst = []
            return_lst = self.peewee_db.consulta_por_id(
                self.mensaje_separado_lst[1]
            )
            print("Listo Consulta por ID de Producto")
            status_lst += (
                return_lst  # adiciona a la lista status lo que devuelve crud
            )

        elif self.mensaje_separado_lst[0] == chr(READ_LST_CHAR):  # "«"ls
            print("Elegido Consulta de Listado de Productos")
            return_lst = []
            return_lst = self.peewee_db.consulta()
            print("Listo Consulta de Listado de Productos")
            status_lst += (
                return_lst  # adiciona a la lista status lo que devuelve crud
            )
            # status_lst.append("OK+D")

        elif self.mensaje_separado_lst[0] == chr(UPDATE_CHAR):  # "^"
            print("Elegido Modificación de Producto")
            return_lst = []
            return_lst = self.peewee_db.modifica(
                (
                    self.mensaje_separado_lst[1],
                    self.mensaje_separado_lst[2],
                    self.mensaje_separado_lst[3],
                    float(self.mensaje_separado_lst[4]),
                )
            )
            print("Listo Modificación de Producto")
            status_lst += (
                return_lst  # adiciona a la lista status lo que devuelve crud
            )
            # status_lst.append(status)

        else:
            status_lst.append((NOK_CHAR,))  # se convierte en tupla

        return status_lst


class CommServidor:
    def __init__(self):
        """
        Inicializa el nodo
        """

        self.message = bytearray()

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()  # IP del servidor
        self.port = 9999  # puerto de escucha

        self.serversocket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )  # solucion a interrumpir el servicio de con Ctrl+C
        self.serversocket.bind(
            (self.host, self.port)
        )  # asocia un socket a una dirección de servidor
        self.serversocket.setblocking(
            0
        )  # modo no bloqueante, relacionado con settimeout()
        print("Host: " + self.host)

    def encendido(self):
        loop_status = True
        connection_status = False
        spinner_status = False

        self.serversocket.listen(3)  # se activa el modo escucha

        while loop_status:
            if connection_status is False:
                if spinner_status is False:
                    spinner.start()
                    spinner_status = True

            try:
                ###
                # Acepta una conexión entrante proveniente de un cliente.
                # Devuelve una conexión abierta entre el servidor y el cliente,
                # junto con la dirección del cliente.
                # La ip del cliente es el primer componente de una tupla.
                ###
                (
                    clientsocket,
                    address,
                ) = self.serversocket.accept()
                connection_status = True
                spinner.stop()
                spinner_status = False
                print(
                    "Se acepta la conexión de {0} con número de conexion {1}.".format(
                        str(address[0]), str(address[1])
                    )
                )

                msg_byte_array = clientsocket.recv(1024)  # mensaje recibido
                print("Mensaje en bruto: {0}".format(msg_byte_array))
                print(
                    "Mensaje decodificado: {0}".format(
                        msg_byte_array.decode("utf-8")
                    )
                )

                # Procesamiento de la información recibida
                desempaquetar = Desempaquetar(msg_byte_array)
                status_lst = desempaquetar.decodificar()
                if status_lst == "empty":
                    print(
                        "No se ha enviado nada. Sólo se estableció la conexión."
                    )
                    print_colour("Presione 'q' para salir", "warning")
                else:
                    status_crud_lst = desempaquetar.operaciones_crud()

                    print(
                        "Tamaño de status_crud_lst: {0}. status_crud_lst: {1}".format(
                            len(status_crud_lst), status_crud_lst
                        )
                    )
                    status_crud_lst = status_crud_lst[
                        ::-1
                    ]  # invierte la lista
                    print("comm_servidor_mod: " + str(status_crud_lst))
                    status_crud_lst = convert_list_of_lists_to_simple_list(
                        status_crud_lst
                    )  # convierte la lista de listas en una simple lista

                    # Se arma el byterray a enviar al cliente
                    packed_data = bytearray()
                    for status_crud_index in status_crud_lst:
                        print(
                            "Convirtiendo {0} en bytes".format(
                                status_crud_index
                            )
                        )
                        if type(status_crud_index) != int:
                            for letter in status_crud_index:
                                packed_data += ord(letter).to_bytes(2, "big")
                        else:
                            packed_data += status_crud_index.to_bytes(2, "big")
                        packed_data += ord("\t").to_bytes(2, "big")
                    clientsocket.send(packed_data)  # se envia la informacion
                    print(
                        "Valores que contesta el servidor: " + str(packed_data)
                    )
                    print_colour("\nPresione 'q' para salir")
                # Bloque que se desplaza
                # clientsocket.close()
                # print("Cerrada la conexión")
                # connection_status = False  # para que vuelva a mostrar el mensaje inicial

            except socket.error as e:
                if e.args[0] == errno.EWOULDBLOCK:
                    time.sleep(1)  # short delay, no tight loops
                else:
                    print("Error no contemplado: {0} ".format(e))
                    spinner.stop()
                    spinner_status = False
                    clientsocket.close()
                    print_colour("Cerrada la conexión.")
                    connection_status = False
                    break

            if key_pressed("q"):
                print_colour("\nPresionada la tecla 'q'", "okgreen")
                spinner.stop()
                spinner_status = False
                if connection_status is True:
                    clientsocket.close()
                    print("Cerrada la conexión")
                    connection_status = False
                else:
                    print(
                        "No es necesario cerrar la conexión. Nunca se abrió."
                    )
                loop_status = False

        print_colour("Servidor apagado")


if __name__ == "__main__":
    comm_servidor = CommServidor()
    comm_servidor.encendido()
    print("FIN")

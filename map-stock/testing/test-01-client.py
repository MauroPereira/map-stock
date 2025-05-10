#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from producto_libs.comm_cliente_mod import CommCliente
from producto_libs.common_libs.char_cons_crud import READ_ID_CHAR

if __name__ == "__main__":
    print(" ***** Client Start ****** \n")

    BLUE = '\033[94m'
    RESET = '\033[0m'

    print(BLUE, end="")
    print("\n-> Creating client instance...\n")
    envio_producto = CommCliente()

    print("\n-> Loading character ID...\n")
    envio_producto.load_data_int(READ_ID_CHAR)  # Request by ID

    print("\n-> Loading ID '1'...\n")
    envio_producto.load_data_str("1")  # ID 1

    print("\n-> Sending and receiving data...\n")
    envio_producto.send_and_receive_data()

    print("\n-> Printing received data...\n")
    envio_producto.print_received_data()

    print("\n-> Checking received data...\n")
    envio_producto.check_received_data()

    print("\n-> Erasing sent and received data...\n")
    envio_producto.erase_sent_and_received_data()

    print("\n-> Closing connection...\n")
    envio_producto.close_conection()

    print(RESET, end="")
    print("\n ***** Client End ****** \n") 
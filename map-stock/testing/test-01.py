#!/usr/bin/env python3
import subprocess
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from producto_libs.comm_cliente_mod import CommCliente
from producto_libs.common_libs.char_cons_crud import READ_ID_CHAR

def run_script(script_path):
    try:
        # Get the absolute path of the script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        full_path = os.path.join(project_root, script_path)
        
        print(f"Executing: {full_path}")
        process = subprocess.Popen(['python3', full_path])
        return process
    except Exception as e:
        print(f"Error executing {script_path}: {str(e)}")
        sys.exit(1)

def run_server():
    # Start the server without blocking execution
    server_process = run_script('producto_libs/comm_servidor_mod.py')
    time.sleep(2)  # Give the server a moment to start up 
    return server_process



if __name__ == "__main__":
    print(" ***** Start ****** \n")

    BLUE = '\033[94m'
    RESET = '\033[0m'

    # Start the server in the background
    server_process = run_server()

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

    # Optionally terminate the server process at the end
    server_process.terminate()
    server_process.wait()

    print("\n ***** End ****** \n")

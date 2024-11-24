# from tkinter import Tk
# from vista import MainApp

# ##########################################################################################
#
# ENTREGA FINAL CURSO PYTHON NIVEL AVANZADO UTNBA 2021
# PROGRAMA: GESTIÓN DE PRODUCTOS - SERVIDOR
#
# Integrantes:
#   • Maria Florencia Lascano Gandulfo – DNI: 31222890 - e-mail: florencialascano@gmail.com
#   • Santiago Nahuel Giay Argañaraz – DNI: 35247374 - e-mail: nahu_3_6@hotmail.com
#   • León David Acosta – DNI: 44216761 - e-mail: leonacosta41@gmail.com
#   • Mauro Alejandro Pereira – DNI: 32297892 - e-mail: mauro.a.pereira@gmail.com
#
# ##########################################################################################

import os
import sys
import subprocess
import threading
from pathlib import Path

# VARIABLES GLOBALES
theproc1 = ""
theproc2 = ""


raiz = Path(__file__).resolve().parent
ruta_server = os.path.join(raiz, "producto_libs", "comm_servidor_mod.py")
print("Ruta del servidor: " + str(ruta_server))
ruta_controller = os.path.join(raiz, "controller.py")
print("Ruta del controller: " + str(ruta_controller))


def encender_servidor():
    if theproc1 != "":
        theproc1.kill()

    hilo_servidor = threading.Thread(
        target=subproceso_servidor(), args=(True,), daemon=True
    )

    hilo_servidor.start()


def encender_controller():
    if theproc2 != "":
        theproc2.kill()

    hilo_controller = threading.Thread(
        target=subproceso_controller(), args=(True,), daemon=True
    )

    hilo_controller.start()


def subproceso_servidor():
    """
    Lanza el servidor como un subproceso
    """

    try:
        global theproc1
        theproc1 = subprocess.Popen([sys.executable, ruta_server])
        theproc1.communicate()

    except Exception as err:
        print(f"Error en el subproceso servidor: {err}")


def subproceso_controller():
    """
    Lanza el controlador como un subproceso
    """

    try:
        global theproc2
        theproc2 = subprocess.Popen([sys.executable, ruta_controller])
        theproc2.communicate()

    except Exception as err:
        print(f"Error en el subproceso controlador: {err}")


if __name__ == "__main__":
    encender_servidor()
    encender_controller()

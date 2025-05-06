#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from producto_libs.comm_servidor_mod import CommServidor

if __name__ == "__main__":
    print(" ***** Server Start ****** \n")
    
    comm_servidor = CommServidor()
    comm_servidor.encendido()
    
    print("\n ***** Server End ****** \n") 
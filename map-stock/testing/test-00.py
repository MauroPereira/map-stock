import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from producto_libs.adv_libs.peewee_mod import PeeweeDb, BoardsTable

if __name__ == "__main__":
    print(" ***** Inicio ****** \n")

    prueba_db = PeeweeDb()

    print("\nCreating placaUno:")
    placaUno = BoardsTable("placaUno")

    print("\nCreating placaDos:")
    placaDos = BoardsTable("placaDos")

    print("\nCreating component MAP-RES in placaDos:")
    placaDos.create(("MAP-RES", 5.0))

    print("\nReading placaDos id=1:")
    print(placaDos.read(id=1))

    print(("\nAlta MAP-RES in placaDos:"))
    prueba_db.alta(("MAP-RES", 80.8, "Resistencia", "Celcius", "0.123"))
    
    print("\nCreating component MAP-RES in placaDos:")
    placaDos.create(("MAP-RES", 5.0))
    
    print("\nReading placaDos id=1:")
    print(placaDos.read(id=1))

    print("\nReading placaDos id=0:")
    print(placaDos.read(id=0))

    print(" ***** Fin ****** ")
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from producto_libs.adv_libs.peewee_mod import PeeweeDb, BoardsTable

if __name__ == "__main__":
    print(" ***** Inicio ****** \n")

    prueba_db = PeeweeDb()
    placaUno = BoardsTable("placaUno")
    placaDos = BoardsTable("placaDos")
    placaDos.create(("MAP-RES", 5.0))
    print(placaDos.read(id=1))
    prueba_db.alta(("MAP-RES", 80.8, "Resistencia", "Celcius", "0.123"))
    placaDos.create(("MAP-RES", 5.0))
    print(placaDos.read(id=1))
    print(placaDos.read())

    print(" ***** Fin ****** ")
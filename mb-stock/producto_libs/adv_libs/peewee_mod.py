import os
import sys
import inspect
from peewee import FloatField
from peewee import SqliteDatabase
from peewee import TextField
from peewee import Model
from peewee import PrimaryKeyField
from peewee import DoesNotExist
from peewee import ForeignKeyField

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from common_libs.char_cons_crud import ID_NF_CHAR
from common_libs.char_cons_crud import NOK_CHAR
from common_libs.char_cons_crud import OK_CHAR
from common_libs.char_cons_crud import UNK_ERROR_CHAR
from common_libs.char_cons_crud import OKD_CHAR

print("\nName in peewee_mod.py:" + str(__name__))

if __name__ == "__main__":
    from decorator_mod import decorador_log
    from conv_lista_de_lista_mod import conv_lista_de_lista

elif __name__ == "adv_libs.peewee_mod":
    from adv_libs.decorator_mod import decorador_log
    from adv_libs.conv_lista_de_lista_mod import conv_lista_de_lista

elif __name__ == "producto_libs.adv_libs.peewee_mod":
    from producto_libs.adv_libs.decorator_mod import decorador_log
    from producto_libs.adv_libs.conv_lista_de_lista_mod import (
        conv_lista_de_lista,
    )

db_name: "name de la base de datos" = "../../database/bd.db"

try:
    db_path = os.path.dirname(os.path.abspath(__file__)) + "/" + db_name
    print("db_path DB: " + db_path)
    mi_base = SqliteDatabase(db_path)

    def make_table_name(model_class):
        """
        Función que devuelve un name de la tabla en base al name de la clase
        """

        model_name = model_class.__name__  # se obtiene el name de la clase
        return model_name.lower() + "_tbl"

    class BaseModel(Model):
        """
        Necesario 1: heredar la clase Model de Peewee
        """

        class Meta:
            """
            Necesario 2: redefinir la clase Meta y definir el atributo
            'database' de dicha clase.
            """

            database = mi_base
            table_function = make_table_name  # llama a la funcion renombrar

    class Components(BaseModel):
        """
        Clase que se convertira en la tabla y en la cual se definen
        los campos.
        """

        ####
        # A replicar:
        #
        # query = """ CREATE TABLE IF NOT EXISTS Components
        #        ( id INTEGER PRIMARY KEY
        #        , description TEXT
        #        , supplier TEXT
        #        , price REAL ) """
        ####

        id = PrimaryKeyField(null=False)
        name = TextField(null=False)
        quantity = FloatField(null=False)
        description = TextField(null=False)
        supplier = TextField(null=False)
        price = FloatField(null=False)

    class Placas(BaseModel):
        """
        Clase que se convertira en la tabla y en la cual se definen
        los campos.
        """

        id = PrimaryKeyField(null=False)
        component_name = ForeignKeyField(Components, to_field="name")
        quantity = FloatField(null=False)

    mi_base.connect()
    mi_base.create_tables([Components])  # por defecto crea una tabla Components
    print(
        "peweee_mod: Base de datos sqlite3 con peewee creada y/o conectada "
        "exitosamente.\n"
    )
except Exception as err:
    raise TypeError(
        f"peweee_mod: Error al intentar crear la db sqlite3 con peewee: {err}"
    )


class PeeweeDb:
    """
    Clase que realiza las funciones CRUD a traves de Peewee
    """

    def __init__(self):
        """
        Imprime un mensaje informativo solamente
        """
        print("peweee_mod: Elegido modo Peewee")

    @decorador_log
    def consulta(self):
        """
        Método que se encarga de obtener información de la base de datos para
        devolverma en forma de lista. En caso de error lanza una expeción y
        retorna una lista vacía.
        """

        # Modo Peewee Sqlite3
        print("peweee_mod: Registros consultados.")  # BUG
        lista_datos = []

        try:
            for datos in Components.select():
                lista_datos.append(
                    (
                        str(datos.id),
                        str(datos.description),
                        str(datos.supplier),
                        str(datos.price),
                    )
                )
            lista_datos.append((OK_CHAR,))  # se convierte en tupla
            print("Registros consultados exitosamente")
        except Exception as error:
            print("Error en peewee desconocido: {0}.".format(error))
            return UNK_ERROR_CHAR

        print(lista_datos)
        return conv_lista_de_lista(lista_datos)

    @decorador_log
    def consulta_por_id(self, consulta_id: "id a devolver" = 1):
        """
        Método que se encarga de obtener información según un id específico,
        de la base de datos para devolverma en forma de lista. En caso de error
        lanza una expeción y retorna una lista vacía.
        """

        # Modo Peewee Sqlite3
        print("peweee_mod: Registros consultados por id.")
        lista_datos = []

        try:
            datos = Components.get(Components.id == consulta_id)
            lista_datos.append(
                (
                    str(datos.id),
                    str(datos.description),
                    str(datos.supplier),
                    str(datos.price),
                )
            )
            lista_datos.append((OKD_CHAR,))  # se convierte en tupla
        except Components.DoesNotExist:
            print("Error en peewee: No existe el ID")
            lista_datos.append(
                (
                    consulta_id,
                    str("NOT FOUND"),
                    str("NOT FOUND"),
                    str("0.0"),
                )
            )
            lista_datos.append((ID_NF_CHAR,))  # se convierte en tupla
        except Exception as error:
            print("Error en peewee desconocido: {0}.".format(error))
            lista_datos.append(
                (
                    consulta_id,
                    str("UNKNOWN ERROR"),
                    str("UNKNOWN ERROR"),
                    str("0.0"),
                )
            )
            lista_datos.append((UNK_ERROR_CHAR,))  # se convierte en tupla
        return conv_lista_de_lista(lista_datos)

    @decorador_log
    def modifica(self, datos: "tupla" = (3, "Lechuga", "Abasto", 50.2)):
        """
        Método que se encarga de actualizar información en la db.
        """

        # Chequea que el primer parámetro sea una tupla. Esto es necesario
        # porque en las intrucciones de crud sobre la base de datos se utiliza
        # formateo de cadenas con tuplas.
        if type(datos) != tuple:
            raise TypeError("El primer parámetro no es una tupla.")

        # Modo Peewee Sqlite3
        lista_datos = []

        try:
            datos_a_actualizar = Components.update(
                description=datos[1], supplier=datos[2], price=datos[3]
            ).where(Components.id == datos[0])
            cant = datos_a_actualizar.execute()
            print("peweee_mod: Registros actualizados: " + str(cant))
            if cant == 0:
                print("Error en peewee: No existe el ID")
                lista_datos.append((ID_NF_CHAR,))  # se convierte en tupla
            else:  # no hay error
                lista_datos.append((OK_CHAR,))  # se convierte en tupla
        except Exception as error:
            print("Error en peewee desconocido: {0}.".format(error))
            lista_datos.append((UNK_ERROR_CHAR,))  # se convierte en tupla
        return conv_lista_de_lista(lista_datos)

    @decorador_log
    def baja(self, datos: "id a borrar" = 6):
        """
        Método que se encarga eliminar información en la db.
        """

        # Modo Peewee Sqlite3
        print("peweee_mod: Registro eliminado por id.")
        lista_datos = []

        try:
            datos_a_borrar = Components.get_by_id(datos)
            datos_a_borrar.delete_instance()
            print(
                "peweee_mod: Registros restantes luego de la eliminación: "
                + str(Components.select().count())
            )
            lista_datos.append((OK_CHAR,))  # se convierte en tupla
        except DoesNotExist:
            print("Error en peewee: No existe el ID")
            lista_datos.append((ID_NF_CHAR,))  # se convierte en tupla
        except Exception as error:
            print("Error en peewee desconocido: {0}.".format(error))
            lista_datos.append((UNK_ERROR_CHAR,))  # se convierte en tupla
        print("comm_servidor_mod.py:lista_datos: {0}".format(lista_datos))
        return conv_lista_de_lista(lista_datos)

    # @decorador_log
    def alta(
        self,
        datos: "tupla" = ("MB-TR", 50.2, "Transistor", "Elemon", "0.055"),
    ):
        """
        Método que se encarga insertar información en la db.
        """

        # Chequea que el primer parámetro sea una tupla. Esto es necesario
        # porque en las intrucciones de crud sobre la base de datos se utiliza
        # formateo de cadenas con tuplas.
        if type(datos) != tuple:
            raise TypeError("El primer parámetro no es una tupla.")

        # Modo Peewee Sqlite3
        lista_datos = []

        tabla_db = Components()
        tabla_db.name = datos[0]
        tabla_db.quantity = datos[1]
        tabla_db.description = datos[2]
        tabla_db.supplier = datos[3]
        tabla_db.price = datos[4]
        cant = tabla_db.save()
        if cant != 0:
            print("peweee_mod: Registros agregados: " + str(cant))
            lista_datos.append((OK_CHAR,))  # se convierte en tupla
        else:  # error inesperado
            lista_datos.append((NOK_CHAR,))  # se convierte en tupla
        return conv_lista_de_lista(lista_datos)

    def presenta_lista(self, lista: "lista" = []):
        """
        Método simple que se encarga de presentar en pantalla una lista
        """
        print("peewee_mod: Presentación de lista:")

        try:
            for datos in lista:
                print(
                    "{0:5} {1:15} {2:20} {3}".format(
                        str(datos[0]), datos[1], datos[2], str(datos[3])
                    )
                )

        except Exception as error:
            print("Error en peewee desconocido: {0}.".format(error))


class BoardsTable:
    """
    Clase que crea una tabla board
    """

    def __init__(self, board_name="PlacaDisplay"):
        self.board_name = board_name  # atributo que define el name de la nueva placa

    def createBoard(self):
        """
        Método se crea la nueva tabla Placa
        """
        try:
            print("hello")
            NewBoard = type(
                "pepe", (Boards,), {}
            )  # se crea el nuevo tipo y se referencia a NuevaPlaca
            print("hello")
            database.create_tables[(NewBoard)]
            print("hello")
            self.board_name2 = NewBoard()  # se reutiliza el atributo
        except Exception as error:
            print("Error al crear nueva tabla Boards: {0}.".format(error))

    def create(
        self,
        datas: "tupla" = ("MB-TR", 0.0),
    ):
        """
        Método que se encarga insertar información en un tipo de tabla Boards
        """

        # Chequea que el primer parámetro sea una tupla. Esto es necesario
        # porque en las intrucciones de crud sobre la base de datos se utiliza
        # formateo de cadenas con tuplas.
        if type(datas) != tuple:
            raise TypeError("El primer parámetro no es una tupla.")

        # Modo Peewee Sqlite3
        data_list = []

        self.board_name.component_name = data_list[0]
        self.board_name.quantity = data_list[1]
        quantity = self.board_name.save()

        if quantity != 0:
            print("peweee_mod: Registros agregados: " + str(quantity))
            data_list.append((OK_CHAR,))  # se convierte en tupla
        else:  # error inesperado
            data_list.append((NOK_CHAR,))  # se convierte en tupla
        return conv_lista_de_lista(data_list)


if __name__ == "__main__":
    from decorator_mod import decorador_log

    print(" ***** Inicio ****** \n")

    cont = 0
    prueba_db = PeeweeDb()
    print(str(cont) + " " + 100 * "-" + " " + str(cont))
    cont = cont + 1

    prueba_db.alta()
    prueba_db.alta(("MB-RES", 80.8, "Resistencia", "Celcius", "0.123"))

    # Ingresa el nombre de la placa
    nombre_placa = "PlacaDisplay22"

    NuevaPlaca = type(nombre_placa, (Placas,), {})

    mi_base.create_tables([NuevaPlaca])

    nombre_placa = NuevaPlaca()  # necesario

    nombre_placa.component_name = "MB-TR"
    nombre_placa.quantity = 2.0
    nombre_placa.save()

    nombre_placa.component_name = "MB-RES"
    nombre_placa.quantity = "5.0"
    nombre_placa.save()

    # se crea la nueva tabla Placa
    # BoardsTable.alta()  # se guarda informacion por defecto
    # BoardsTable.alta(("MB-RES", "5.0"))  # se guarda información

    """    
    prueba_db.alta()
    print(str(cont) + " " + 100 * "-" + " " + str(cont))
    cont = cont + 1  # 1

    lista = prueba_db.consulta()
    prueba_db.presenta_lista(lista)
    print(str(cont) + " " + 100 * "-" + " " + str(cont))
    cont = cont + 1  # 1

    prueba_db.alta()
    print(str(cont) + " " + 100 * "-" + " " + str(cont))
    cont = cont + 1  # 2

    lista = prueba_db.consulta()
    prueba_db.presenta_lista(lista)
    print(str(cont) + " " + 100 * "-" + " " + str(cont))
    cont = cont + 1  # 3
    """

    # lista = prueba_db.consulta_por_id(100)
    # prueba_db.presenta_lista(lista)
    # print(str(cont) + " " + 100 * "-" + " " + str(cont))
    # cont = cont + 1  # 4

    """
    prueba_db.baja(34)
    print(str(cont) + " " + 100 * "-" + " " + str(cont))
    cont = cont + 1
    
    lista = prueba_db.consulta()
    prueba_db.presenta_lista(lista)
    print(str(cont) + " " + 100 * "-" + " " + str(cont))
    cont = cont + 1  # 6

    prueba_db.alta(("Sapallo", "Huertaaa organicaaa", 20.8))
    print(str(cont) + " " + 100 * "-" + " " + str(cont))
    cont = cont + 1  # 7

    lista = prueba_db.consulta()
    prueba_db.presenta_lista(lista)
    print(str(cont) + " " + 100 * "-" + " " + str(cont))
    cont = cont + 1  # 8
    
    prueba_db.modifica(((100, "Zapallo", "Huerta organica", 25.5)))
    print(str(cont) + " " + 100 * "-" + " " + str(cont))
    cont = cont + 1  # 9

    lista = prueba_db.consulta()
    prueba_db.presenta_lista(lista)
    print(str(cont) + " " + 100 * "-" + " " + str(cont))
    cont = cont + 1  # 10

    prueba_db.baja(7)
    print(str(cont) + " " + 100 * "-" + " " + str(cont))
    cont = cont + 1  # 11

    prueba_db.baja(6)
    print(str(cont) + " " + 100 * "-" + " " + str(cont))
    cont = cont + 1  # 12

    lista = prueba_db.consulta()
    prueba_db.presenta_lista(lista)
    print(str(cont) + " " + 100 * "-" + " " + str(cont))
    cont = cont + 1  # 13
    
    prueba_db.baja()
    print(str(cont) + " " + 100 * "-" + " " + str(cont))
    cont = cont + 1  # 5
    """

    print(" ***** Fin ****** ")

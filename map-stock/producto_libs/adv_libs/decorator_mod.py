import datetime
import os
import sys
import inspect

currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe()))
)
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from common_libs.char_cons_crud import ID_NF_CHAR
from common_libs.char_cons_crud import UNK_ERROR_CHAR
from common_libs.char_cons_crud import NOK_CHAR


def log_to_file(
    nombre_archivo: "nombre del archivo log" = "producto_python.log",
    entrada_info: "string con la informacion a guardar" = "prueba",
):
    """
    Función que se encarga de guardar datos en un fichero
    """

    ruta = os.path.dirname(os.path.abspath(__file__)) + "/" + nombre_archivo

    try:
        f = open(ruta, "a")
        f.write(entrada_info + "\n")
        f.close()
    except TypeError as err:
        print(f"Error al guardar en log: {err}")


def decorador_log(funcion_a_envolver):
    """
    Decorador que funciona como log, al cual se le puede agregar informacion
    extra y definir si retorna.
    """

    def _decorador_log(*args, **kwargs):
        funcion_valida = True
        datos_en_decorador = ""

        retorno_de_envolver = funcion_a_envolver(*args, **kwargs)

        print("\n" + 15 * "*")
        tipo_crud = str(funcion_a_envolver.__name__)
        print("Funcion en el decorador: " + tipo_crud)

        if tipo_crud == "alta":
            if len(args) > 1:
                datos_en_decorador = args[1]
            else:
                datos_en_decorador = funcion_a_envolver.__defaults__[0]
            datos_en_decorador = str(
                "Descr: "
                + datos_en_decorador[0]
                + ", Provee: "
                + datos_en_decorador[1]
                + ", Precio: "
                + str(datos_en_decorador[2])
            )
            print("Datos en decorador: " + datos_en_decorador)

        elif tipo_crud == "baja":
            # Obtiene el ID
            if len(args) > 1:
                datos_en_decorador = str(args[1])
            else:
                datos_en_decorador = str(
                    funcion_a_envolver.__defaults__[0]
                )  # toma el argumento por defecto

            # Chequea que no se haya producido un error
            print("retorno_de_envolver: {0}".format(retorno_de_envolver))
            if retorno_de_envolver == ID_NF_CHAR:  # error ID no encontrado
                datos_en_decorador += " NOT FOUND"
            elif retorno_de_envolver == UNK_ERROR_CHAR:  # error desconocido
                datos_en_decorador += " UNKNOWN ERROR!"

            datos_en_decorador = "ID eliminado: " + datos_en_decorador
            print("Datos en decorador: " + datos_en_decorador)

        elif tipo_crud == "consulta":
            datos_en_decorador = ""
            for datos in retorno_de_envolver:
                if len(datos) != 1:
                    datos_en_decorador = (
                        datos_en_decorador
                        + "ID: "
                        + str(datos[0])
                        + ", Descr: "
                        + datos[1]
                        + ", Provee: "
                        + datos[2]
                        + ", Precio: "
                        + str(datos[3])
                        + str(" |\t")
                    )
                else:
                    print("Resultado de la operación crud: {0}".format(datos))
                    if datos == NOK_CHAR:  # error operacion sin exito
                        datos_en_decorador += " NO OK CHAR"
                    elif datos == UNK_ERROR_CHAR:  # error desconocido
                        datos_en_decorador += " UNKNOWN ERROR!"

            print("Datos en decorador: " + datos_en_decorador)

        elif tipo_crud == "modifica":
            if len(args) > 1:
                datos_en_decorador = args[1]
            else:
                datos_en_decorador = funcion_a_envolver.__defaults__[0]
            datos_en_decorador = str(
                "ID modificado: "
                + str(datos_en_decorador[0])
                + ", Descr: "
                + datos_en_decorador[1]
                + ", Provee: "
                + datos_en_decorador[2]
                + ", Precio: "
                + str(datos_en_decorador[3])
            )

            if retorno_de_envolver == ID_NF_CHAR:  # error ID no encontrado
                datos_en_decorador += " NOT FOUND"
            elif retorno_de_envolver == UNK_ERROR_CHAR:  # error desconocido
                datos_en_decorador += " UNKNOWN ERROR!"

            print("Datos en decorador: " + datos_en_decorador)

        elif tipo_crud == "consulta_por_id":
            if len(args) > 1:
                datos_en_decorador_ant = args[1]
            else:
                datos_en_decorador_ant = funcion_a_envolver.__defaults__[0]

            datos_en_decorador = ""
            print("retorno_de_envolver: {0}".format(retorno_de_envolver))
            #####
            # BUG: consiste en que por ejemplo para retorno_de_envolver: [[1, 'a', 'b', '2.2'], [49849]]
            #       se le esta pidiendo por medio del bucle que sigue, que recorra el segundo elemento,
            #       el cual tiene un solo elemento, el numero 49849.
            #####
            for datos in retorno_de_envolver:
                if len(datos) != 1:
                    datos_en_decorador = (
                        "ID consultado: "
                        + str(datos_en_decorador_ant)
                        + " <- Descr: "
                        + str(datos[1])
                        + ", Provee: "
                        + datos[2]
                        + ", Precio: "
                        + datos[3]
                        + str("\t")
                    )
                else:
                    print("Resultado de la operación crud: {0}".format(datos))
            print("Datos en decorador: " + datos_en_decorador)

        else:
            print("Funcion no soportada, no se va a registrar")
            funcion_valida = False

        if funcion_valida:
            str_info = datetime.datetime.today().strftime(
                "%y/%m/%d %H:%M:%S - "
                + tipo_crud
                + " -> "
                + datos_en_decorador
            )
            print("\nlog: " + str_info)
            log_to_file(entrada_info=str_info)
        print(15 * "*" + "\n")

        return retorno_de_envolver

    return _decorador_log


"""
Nota: datos_en_decorador = funcion_a_envolver.__defaults__[0] se utiliza  
    para tomar los argumentos por defecto al invocar la funcion
"""


def decorador_deprecrated(funcion_a_envolver):
    """
    Decorador que indica que una funcion o método esta de desuso.
    """

    def _decorador_log(*args, **kwargs):
        retorno_de_envolver = funcion_a_envolver(*args, **kwargs)
        deprecrated = str(funcion_a_envolver.__name__)
        print(
            "La función o método "
            + deprecrated
            + "está en desuso y se eliminará en una "
            "versión futura"
        )

        return retorno_de_envolver

    return _decorador_log


if __name__ == "__main__":
    print("Fin")

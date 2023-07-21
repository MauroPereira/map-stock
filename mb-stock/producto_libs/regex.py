import re
from tkinter.constants import FALSE, NONE


class Regex:
    def __init__(self):
        pass

    @staticmethod
    def comprueba_proveedor(proveedor):
        """
        Comprueba que el nombre del proveedor solo contenga letras.
        """
        pattern = re.compile("^[a-zA-Z]+$")
        comprobador = pattern.match(proveedor)
        if comprobador:
            return True
        else:
            return False

    @staticmethod
    def comprueba_precio(precio):
        """
        Comprueba que el precio sea un numero, independientemente
        de que se un entero o no.
        """
        pattern = re.compile("[-+]?([0-9]*\.[0-9]+|[0-9]+)")
        comprobador = pattern.match(precio)
        if comprobador:
            return True
        else:
            return False

    @staticmethod
    def comprueba_descripcion(producto):
        """
        Comprueba que la descripcion sean solo letras
        """
        pattern = re.compile("^[a-zA-Z]+$")
        comprobador = pattern.match(producto)
        if comprobador:
            return True
        else:
            return False


if __name__ == '__main__':
    o = Regex()
    print(o.comprueba_precio('15.5'))
    print(o.comprueba_precio('ss'))
    print(o.comprueba_descripcion('asad'))
    print(o.comprueba_proveedor('aaa'))

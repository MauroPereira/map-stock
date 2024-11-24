import binascii


def convert_bytearrays_to_str(origin_bytearray: "bytearray a convetir"):
    """
    Convierte un bytearray a un string
    """

    return str(binascii.hexlify(origin_bytearray).decode("utf-8"))


def char_to_bytes(
    origin_char: "char a convetir" = "0xC2B9",
    bytes_numbers: "longitud en bytes" = 2,
    order: "orden de bytes" = "big",
):
    """
    Convierte un char en un bytearray especificando la cantidad de bytes y el tipo de codificación
    """
    return bytearray(origin_char.to_bytes(bytes_numbers, order))


def convert_list_of_lists_to_simple_list(
    list_origin: "lista a convetir" = [
        [33],
        ["100", "NOT FOUND", "NOT FOUND", "0.0"],
    ]
):
    """
    Devuelve una lista de listas en una simple lista
    """

    list_destination = []

    for list_origin_index in list_origin:
        for list_origin_index_index in list_origin_index:
            list_destination.append(list_origin_index_index)
    return list_destination


def convert_bytes_array_to_list(bytes_array_origin: "array a convertir"):
    """
    Devuelve una lista de una array de bytes separados por '\t'"
    """

    str_decode = bytes_array_origin.decode("UTF-8")
    list_decode = str_decode.split("\x00")

    ###
    # Va acumulando en un str temporal hasta toparse con una
    # tabulación, en donde guarda ese temporal en una lista y
    # se reinicia el proceso. Antes de eso, chequea que
    # termine con una tabulación el arreglo de bytes, a fin
    # de que no se pierda información.
    ###
    if list_decode[-1] != "\t":
        list_decode.append("\t")

    list_decode2 = []
    temp_str = ""
    for val in list_decode:
        if val == "\t":
            list_decode2.append(temp_str)
            temp_str = ""
        else:
            temp_str += val

    return list_decode2


if __name__ == "__main__":
    test_ba = bytearray(
        b"\xc2\xb2\x00\t\x001\x000\x00\t\x00a\x00\t\x00b\x00\t\x001\x00.\x001\x00\t"
    )

    print(convert_bytes_array_to_list(test_ba))

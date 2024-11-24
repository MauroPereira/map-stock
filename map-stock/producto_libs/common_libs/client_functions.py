if __name__ == "__main__":
    from char_cons_crud import ID_NF_CHAR
    from char_cons_crud import UNK_ERROR_CHAR
    from char_cons_crud import NOK_CHAR
    from char_cons_crud import OK_CHAR
    from char_cons_crud import OKD_CHAR
    from convert_data_types import char_to_bytes

if __name__ == "producto_libs.common_libs.client_functions":
    from producto_libs.common_libs.char_cons_crud import ID_NF_CHAR
    from producto_libs.common_libs.char_cons_crud import UNK_ERROR_CHAR
    from producto_libs.common_libs.char_cons_crud import NOK_CHAR
    from producto_libs.common_libs.char_cons_crud import OK_CHAR
    from producto_libs.common_libs.char_cons_crud import OKD_CHAR


def check_received(
    str_received: "string recibido a comparar" = "¹",
    ok_message: "mensaje a mostrar para el ok" = "Petición CRUD exitosa",
):
    """
    Se encarga de imprimir mensajes en base al string recibido, con
    la opcion de un mensaje personalizado si todo está ok
    """

    if len(str_received) == 0:
        print("Error del servidor: no se recibio nada!")
    else:
        utf8_received = str_received.encode("utf-8")

        # Se encarga de 'dimensionar' correctamente la variable si es necesario, para la comparación posterior
        if len(utf8_received) == 1:
            utf8_received = (ord(str_received)).to_bytes(2, "big")

        print("Respuesta recibida: {0}".format(utf8_received))

        if utf8_received == ID_NF_CHAR.to_bytes(2, "big"):
            print("ID no encontrado!")
        elif utf8_received == UNK_ERROR_CHAR.to_bytes(2, "big"):
            print("Error desconocido!")
        elif utf8_received == NOK_CHAR.to_bytes(2, "big"):
            print("Petición CRUD no encontrada!")
        elif utf8_received == OK_CHAR.to_bytes(2, "big"):
            print(ok_message)
        elif utf8_received == OKD_CHAR.to_bytes(2, "big"):
            print("Petición CRUD exitosa. Se incluyen datos")
        else:
            print("\nError crítico. Contáctese con soporte!")
    return


if __name__ == "__main__":

    str_message = "!"
    print("String a chequear: {0}".format(str_message))
    check_received(str_message)
    print(15 * "-")
    str_message = "¹"
    print("String a chequear: {0}".format(str_message))
    check_received(str_message)
    print(15 * "-")
    str_message = "²"
    print("String a chequear: {0}".format(str_message))
    check_received(str_message)
    print(15 * "-")
    str_message = "°"
    print("String a chequear: {0}".format(str_message))
    check_received(str_message)
    print(15 * "-")
    str_message = "®"
    print("String a chequear: {0}".format(str_message))
    check_received(str_message)
    print(15 * "-")
    str_message = "a"
    print("String a chequear: {0}".format(str_message))
    check_received(str_message)

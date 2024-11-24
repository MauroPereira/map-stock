def conv_lista_de_lista(lista_con_tuplas):
    """
    Función que se encarga de transformar una lista de tuplas en una lista
    de listas.
    """

    lista = []

    for i in lista_con_tuplas:
        lista.append(list(i))

    return lista


if __name__ == "__main__":
    tuple_list_test = [(1, "a", "b", "2.2"), (49849,)]
    print("Tipo de entrada: {0}".format(type(tuple_list_test)))
    print("Entrada: {0}".format(tuple_list_test))
    lista = conv_lista_de_lista(tuple_list_test)
    print("Salida: {0}".format(lista))
    print("Elementos de salida:")
    for i in lista:
        print(i)

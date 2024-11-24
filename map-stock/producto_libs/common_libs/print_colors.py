class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_colour(
    string_entrante: "string a colorear" = "Ejemplo",
    colour: "tipo de color" = "warning",
):
    """
    Se encarga de colorear el string entrante con un color determinado,
    por defecto o no definido WARNING
    """

    if colour == "okgreen":
        print(bcolors.OKGREEN, end="")
    if colour == "okblue":
        print(bcolors.OKBLUE, end="")
    else:
        print(bcolors.WARNING, end="")

    print(string_entrante)

    print(bcolors.ENDC, end="")

    return


if __name__ == "__main__":
    print_colour()
    print_colour(colour="okblue")
    print_colour(colour="okgreen")

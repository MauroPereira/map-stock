from tkinter import Tk
from vista import MainApp

# ##########################################################################################
#
# Motor: GESTIÓN DE PRODUCTOS - SERVIDOR MAP v1.0
# Programa: MB-STOCK v1.0
#
# Desarrollador:
#   • Mauro Alejandro Pereira <mauro.a.pereira@gmail.com> 
#
# ##########################################################################################


class MiApp:
    def __init__(self, window):
        self.ventana = window
        MainApp(self.ventana)


if __name__ == "__main__":
    root = Tk()
    obj = MiApp(root)
    root.mainloop()

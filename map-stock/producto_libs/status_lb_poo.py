from tkinter import Label


class StatusLb:
    """
    Clase que crea una etiqueta de status
    """

    def __init__(self, window, **config):
        self.window = window
        self.status_lb = Label(self.window, text="")
        self.status_lb.grid(**config)
        self.status_lb.config(fg="red", font=("Courier", 12, "italic"))

    def imprimir_rojo(self, text_str):
        """
        Al contenido de la etiqueta lo sobreescribe en rojo
        """
        self.status_lb.config(fg="red")
        self.status_lb.config(text=text_str)

    def imprimir_verde(self, text_str):
        """
        Al contenido de la etiqueta lo sobreescribe en verde
        """
        self.status_lb.config(fg="green")
        self.status_lb.config(text=text_str)

    def borrar(self):
        """
        Al contenido de la etiqueta lo borra
        """
        self.status_lb.config(text="")

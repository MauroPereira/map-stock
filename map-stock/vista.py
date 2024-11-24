import sys
from tkinter import StringVar
from tkinter import ttk
from tkinter import Frame
from tkinter.constants import CENTER
from tkinter import messagebox
from model import Model
import tkinter as tk
from producto_libs.producto_poo import Producto
from producto_libs.status_lb_poo import StatusLb
from producto_libs.regex import *
from producto_libs.comm_servidor_mod import CommServidor


class MainApp(Frame):
    """
    Clase principal de la aplicación que controla la interfaz de usuario
    """

    def __init__(self, root):
        super().__init__(root)
        self.main_window = root
        self.model = Model()
        self.draw_ui()

    def mostrar_add_frame(self):
        """
        Se encarga de cargar la ventana de Agregar producto
        """
        self.status_lb.borrar()
        add_frame = AddFrame(self.main_window, parent=self, model=self.model)
        add_frame.draw_ui()

    def mostrar_edit_frame(self):
        """
        Se encarga de cargar la ventana de Editar producto
        """
        self.status_lb.borrar()
        selected_id = self.table.item(self.table.selection())["text"]

        if selected_id:
            update_frame = UpdateFrame(
                self.main_window, parent=self, model=self.model
            )
            update_frame.draw_ui(selected_id)
        else:
            print("Debe seleccionar un producto")
            self.status_lb.imprimir_rojo("Debe seleccionar un producto")
            self.after(1000, self.status_lb.borrar)

    def borrar_producto(self):
        """
        Se encarga de cargar la ventana de Borrar producto
        """
        self.status_lb.borrar()
        selected_id = self.table.item(self.table.selection())["text"]

        status_str = self.model.chequear_selected_id(selected_id)

        if status_str == "delete_ok":
            print("Producto borrado con exito")
            self.status_lb.imprimir_verde("Producto borrado con éxito")
            self.lista_productos()
            self.after(1000, self.status_lb.borrar)
        elif status_str == "delete_nok":
            print("Error cargando el producto")
            self.status_lb.imprimir_rojo("Error cargando el producto")
            self.after(1000, self.status_lb.borrar)
        else:
            print("Debe seleccionar un producto")
            self.status_lb.imprimir_rojo("Debe seleccionar un producto")
            self.after(1000, self.status_lb.borrar)

    def draw_ui(self):
        """
        Metodo que carga todos los objetos visuales en la ventana Gestión de productos
        """
        self.main_window.title("Gestión de productos")
        self.main_window.configure(padx=20, pady=20)

        self.frame1 = Frame(self.main_window)
        self.frame2 = Frame(self.main_window)
        self.frame3 = Frame(self.main_window)

        self.frame1.pack(fill="both", expand="yes", padx=20, pady=10)
        self.frame2.pack(fill="both", expand="yes", padx=20, pady=10)
        self.frame3.pack(fill="both", expand="yes", padx=20, pady=10)

        self.modal_list_title = tk.Label(
            self.frame1,
            text="Listado de productos",
            font=("Verdana", 14, "bold"),
        )
        self.modal_list_title.grid(row=0, column=0, columnspan=6)

        self.btn_style = ttk.Style().configure(
            "TButton",
            padding=6,
            background="#FFFFFF",
            foreground="#000000",
            font=("Verdana", 10, "bold"),
        )

        btn_add = ttk.Button(
            self.frame2,
            text="Añadir",
            command=self.mostrar_add_frame,
            style=self.btn_style,
        )
        btn_add.grid(row=1, column=1)

        self.btn_edit = ttk.Button(
            self.frame2, text="Editar", command=self.mostrar_edit_frame
        )
        self.btn_edit.grid(row=1, column=2, columnspan=1)

        self.btn_delete = ttk.Button(
            self.frame2, text="Eliminar", command=self.borrar_producto
        )
        self.btn_delete.grid(row=1, column=3, columnspan=1)

        self.status_lb = StatusLb(self.frame2, row=1, column=4)

        column_headers = ["ID", "DESCRIPCIÓN", "PROVEEDOR", "PRECIO"]

        self.table = ttk.Treeview(
            self.frame3, columns=("#1", "#2", "#3"), height=10
        )

        for index, header in enumerate(column_headers):
            self.table.grid(row=4, column=index)
            self.table.heading("#{}".format(index), text=header, anchor=CENTER)

        self.lista_productos()
        self.main_window.mainloop()

        print("Fin de Producto")

    def borra_treeview(self):
        """Método que borra todos los items"""
        for element in self.table.get_children():
            self.table.delete(element)

    def lista_productos(self):
        self.borra_treeview()
        self.model.llenar_tree_view(self.table)


class AddFrame(Frame):
    """
    Clase que representa el formulario de Alta de productos
    """

    def __init__(self, main_window, parent, model):
        super().__init__(main_window)
        self.main_window = main_window
        self.parent = parent
        self.model = model

    def producto_agregar(self):
        """Método que agrega un producto"""
        producto = Producto(
            id=0,
            descripcion=self.entry_descripcion.get(),
            proveedor=self.entry_proveedor.get(),
            precio=self.entry_precio.get(),
        )

        try:
            status_str = self.model.chequear_agregar_producto(producto)

            if status_str:
                self.parent.lista_productos()
                print("Agregado exitosamente")
                self.status_lb.imprimir_verde("Agregado exitosamente")
                self.destroy()
            else:
                print("Error al agregar")
                self.status_lb.imprimir_rojo("Error al agregar")
        except Exception as e:
            print(f"Error al modificar: {sys.exc_info()[1]}")
            self.status_lb.imprimir_rojo(
                f"Error al modificar: {sys.exc_info()[1]}"
            )

    def draw_ui(self):
        """
        Método que carga todos los objetos visuales en la ventana Alta Productos
        """
        self.main_window_add = tk.Toplevel()

        self.main_window_add.title("Alta Productos")
        self.main_window_add.configure(padx=20, pady=20)

        self.modal_add_label = ttk.Label(
            self.main_window_add,
            text="Alta Productos",
            font=("Verdana", 14, "bold"),
        )
        self.modal_add_label.grid(row=0, column=1, columnspan=5)

        ttk.Label(self.main_window_add, text="Descripcion", width=20).grid(
            row=1, column=1, columnspan=2
        )

        self.entry_descripcion = ttk.Entry(self.main_window_add, width=40)
        self.entry_descripcion.grid(row=1, column=3, columnspan=3)

        ttk.Label(self.main_window_add, text="Proveedor", width=20).grid(
            row=2, column=1, columnspan=2
        )

        self.entry_proveedor = ttk.Entry(self.main_window_add, width=40)
        self.entry_proveedor.grid(row=2, column=3, columnspan=3)

        ttk.Label(self.main_window_add, text="Precio", width=20).grid(
            row=3, column=1, columnspan=2
        )

        self.entry_precio = ttk.Entry(self.main_window_add, width=40)
        self.entry_precio.grid(row=3, column=3, columnspan=3)

        self.btn_add_product = ttk.Button(
            self.main_window_add, text="Agregar", command=self.producto_agregar
        )
        self.btn_add_product.grid(row=4, column=1, columnspan=5)

        self.status_lb = StatusLb(self.main_window_add, row=5, columnspan=6)

        self.main_window_add.mainloop()


class UpdateFrame(Frame):
    """
    Clase que representa el formulario de modificación
    """

    def __init__(self, main_window, parent, model):
        super().__init__(main_window)
        self.main_window = main_window
        self.parent = parent
        self.model = model

    def draw_ui(self, selected_id):
        """
        Método que carga todos los objetos visuales en la ventana Editar productos
        """
        producto = self.model.producto_get_by_id(selected_id)

        self.main_window_edit = tk.Toplevel()

        self.main_window_edit.title("Editar productos")
        self.main_window_edit.configure(padx=20, pady=20)

        ttk.Label(
            self.main_window_edit,
            text="Modificación de productos",
            font=("Verdana", 14, "bold"),
        ).grid(row=0, column=0, columnspan=2)

        tk.Label(self.main_window_edit, text="Id").grid(row=1, column=0)

        self.entry_id = tk.Entry(
            self.main_window_edit,
            textvariable=StringVar(self.main_window_edit, value=producto.id),
            state="readonly",
            width=30,
        )
        self.entry_id.grid(row=1, column=1)

        tk.Label(self.main_window_edit, text="Nombre").grid(row=2, column=0)

        self.entry_descripcion = tk.Entry(
            self.main_window_edit,
            textvariable=StringVar(
                self.main_window_edit, value=producto.descripcion
            ),
            width=30,
        )
        self.entry_descripcion.grid(row=2, column=1)

        tk.Label(self.main_window_edit, text="Proveedor").grid(row=3, column=0)

        self.entry_proveedor = tk.Entry(
            self.main_window_edit,
            textvariable=StringVar(
                self.main_window_edit, value=producto.proveedor
            ),
            width=30,
        )
        self.entry_proveedor.grid(row=3, column=1)

        tk.Label(self.main_window_edit, text="Precio").grid(row=4, column=0)

        self.entry_precio = tk.Entry(
            self.main_window_edit,
            textvariable=StringVar(
                self.main_window_edit, value=producto.precio
            ),
            width=30,
        )
        self.entry_precio.grid(row=4, column=1)

        self.btn = ttk.Button(
            self.main_window_edit,
            text="Actualizar",
            command=self.producto_editar,
        ).grid(row=5, column=0, columnspan=2)

        self.status_lb = StatusLb(self.main_window_edit, row=6, columnspan=6)

        self.main_window_edit.mainloop()

    def producto_editar(self):
        """
        Método que edita un producto
        """
        producto = Producto(
            id=self.entry_id.get(),
            descripcion=self.entry_descripcion.get(),
            proveedor=self.entry_proveedor.get(),
            precio=self.entry_precio.get(),
        )
        try:
            status_str = self.model.chequear_actualizar_producto(producto)
            if status_str:
                print("Modificado exitosamente")
                self.parent.lista_productos()
                self.status_lb.imprimir_verde("Modificado exitosamente")
                self.destroy()
            else:
                print("Error al modificar")
                self.status_lb.imprimir_rojo("Error al modificar")
        except Exception as e:
            print(f"Error al modificar: {sys.exc_info()[1]}")
            self.status_lb.imprimir_rojo(
                f"Error al modificar: {sys.exc_info()[1]}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root=root)
    app.mainloop()

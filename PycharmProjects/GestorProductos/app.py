import tkinter as tk
from tkinter import ttk, LabelFrame, Label, Entry, W, E
import sqlite3

class Producto:
    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(1, 1)
        self.ventana.wm_iconbitmap('recursos/icon.ico')

        # Frame principal
        frame = ttk.Frame(self.ventana)
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Widgets de entrada
        self.etiqueta_nombre = Label(frame, text="Nombre: ", font=('Calibri', 15, 'bold'))
        self.etiqueta_nombre.grid(row=1, column=0)
        self.nombre = Entry(frame, font=('Calibri', 16, 'bold'))
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        self.etiqueta_precio = Label(frame, text="Precio: ", font=('Calibri', 15, 'bold'))
        self.etiqueta_precio.grid(row=2, column=0)
        self.precio = Entry(frame, font=('Calibri', 16, 'bold'))
        self.precio.grid(row=2, column=1)

        # Botón de guardar debajo de nombre y precio
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto, style='my.TButton')
        self.boton_aniadir.grid(row=3, column=0, columnspan=2, pady=10, sticky=W + E)

        # Ruta de la base de datos
        self.db = 'database/productos.db'

        # Tabla para representar el widget
        self.tabla = ttk.Treeview(frame, columns=('Nombre', 'Precio'))
        self.tabla.grid(row=4, columnspan=2)

        # Configurar el estilo para el encabezado
        style = ttk.Style()
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))

        # Mostrar los títulos en la tabla
        self.tabla.heading('#0', text="Nombre", anchor=tk.E)
        self.tabla.heading('#1', text="Precio", anchor=tk.E)

        # Llamada al método get_productos() al inicio de la app
        self.get_productos()

        # Botones de acción
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))

        boton_eliminar = ttk.Button(text='ELIMINAR', command=self.del_producto, style='my.TButton')
        boton_eliminar.grid(row=6, column=0, sticky=W + E)

        boton_editar = ttk.Button(text='EDITAR', command=self.edit_producto, style='my.TButton')
        boton_editar.grid(row=6, column=1, sticky=W + E)

        boton_mostrar_terminal = ttk.Button(text='Mostrar productos por terminal', command=self.mostrar_productos_terminal, style='my.TButton')
        boton_mostrar_terminal.grid(row=7, columnspan=2, sticky=W + E)

        # Mensaje informativo para el usuario
        self.mensaje = tk.Label(text='', fg='red')
        self.mensaje.grid(row=5, column=0, columnspan=2, sticky=W + E)

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            cursor.execute(consulta, parametros)
            resultados = cursor.fetchall()

        return resultados

    def get_productos(self):
        # Limpiar la tabla al iniciar la app
        self.tabla.delete(*self.tabla.get_children())

        # Consulta SQL
        query = 'SELECT * FROM producto ORDER BY nombre DESC'
        registros_db = self.db_consulta(query)

        # Mostrar los resultados en la tabla y por consola
        for fila in registros_db:
            self.tabla.insert('', 'end', values=(fila[1], fila[2]))

    def mostrar_productos_terminal(self):
        # Consulta SQL
        query = 'SELECT * FROM producto ORDER BY nombre DESC'
        registros_db = self.db_consulta(query)

        # Mostrar los resultados en la terminal
        for fila in registros_db:
            print(fila)

    def validacion_nombre(self):
        return bool(self.nombre.get())

    def validacion_precio(self):
        return bool(self.precio.get())

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio():
            query = 'INSERT INTO producto VALUES(NULL, ?, ?)'  # Consulta SQL (sin los datos)
            parametros = (self.nombre.get(), self.precio.get())  # Parámetros de la consulta SQL
            self.db_consulta(query, parametros)
            self.mensaje['text'] = 'Producto {} añadido con éxito'.format(self.nombre.get())
            self.get_productos()  # Actualizar la tabla después de añadir un producto
            self.nombre.delete(0, tk.END)  # Borrar el campo nombre del formulario
            self.precio.delete(0, tk.END)  # Borrar el campo precio del formulario
        else:
            self.mensaje['text'] = 'El nombre y el precio son obligatorios'

    def del_producto(self):
        # Mensaje inicialmente vacío
        self.mensaje['text'] = ''

        # Comprobación de que se seleccione un producto para poder eliminarlo
        seleccion = self.tabla.selection()
        if not seleccion:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        nombre = self.tabla.item(seleccion)['values'][0]
        query = 'DELETE FROM producto WHERE nombre = ?'  # Consulta SQL
        self.db_consulta(query, (nombre,))
        self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.get_productos()  # Actualizar la tabla de productos

    def edit_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacío
        seleccion = self.tabla.selection()

        try:
            nombre_seleccionado = self.tabla.item(seleccion)['values'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        self.mensaje['text'] = ''
        nombre = self.tabla.item(seleccion)['values'][0]
        old_precio = self.tabla.item(seleccion)['values'][1]  # El precio se encuentra dentro de una lista

        # Crear una ventana de edición
        self.ventana_editar = tk.Toplevel()
        self.ventana_editar.title("Edición de productos")  # Título nuevo
        self.ventana_editar.resizable(1, 1)
        self.ventana_editar.wm_iconbitmap('recursos/icon.ico')

        # Agregar título en negrita grande
        titulo = Label(self.ventana_editar, text="Edición de productos", font=("Arial", 14, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)

        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto", font=('Calibri', 16, 'bold'))
        frame_ep.grid(row=1, column=0, columnspan=2, pady=20)

        # Mostrar valores actuales
        tk.Label(frame_ep, text="Nombre antiguo: ", font=('Calibri', 13)).grid(row=0, column=0)
        tk.Entry(frame_ep, state='readonly', textvariable=tk.StringVar(value=nombre), font=('Calibri', 13)).grid(row=0, column=1)

        tk.Label(frame_ep, text="Precio antiguo: ", font=('Calibri', 13)).grid(row=1, column=0)
        tk.Entry(frame_ep, state='readonly', textvariable=tk.StringVar(value=old_precio), font=('Calibri', 13)).grid(row=1, column=1)

        tk.Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13)).grid(row=2, column=0)
        nuevo_nombre_entry = tk.Entry(frame_ep, font=('Calibri', 13))
        nuevo_nombre_entry.grid(row=2, column=1)

        tk.Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13)).grid(row=3, column=0)
        nuevo_precio_entry = tk.Entry(frame_ep, font=('Calibri', 13))
        nuevo_precio_entry.grid(row=3, column=1)

        nuevo_nombre_entry.insert(0, nombre)
        nuevo_precio_entry.insert(0, old_precio)

        # Boton Actualizar Producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", style='my.TButton',
                                           command=lambda: self.actualizar_productos(nombre, nuevo_nombre_entry.get(),
                                                                                    nuevo_precio_entry.get(), old_precio))
        self.boton_actualizar.grid(row=4, columnspan=2, sticky=W + E)

    def actualizar_productos(self, antiguo_nombre, nuevo_nombre, nuevo_precio, antiguo_precio):
        producto_modificado = False
        query = 'UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?'

        if nuevo_nombre != '' and nuevo_precio != '':
            # Si el usuario escribe nuevo nombre y nuevo precio, se cambian ambos
            parametros = (nuevo_nombre, nuevo_precio, antiguo_nombre, antiguo_precio)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '':
            # Si el usuario deja vacío el nuevo precio, se mantiene el precio anterior
            parametros = (nuevo_nombre, antiguo_precio, antiguo_nombre, antiguo_precio)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '':
            # Si el usuario deja vacío el nuevo nombre, se mantiene el nombre anterior
            parametros = (antiguo_nombre, nuevo_precio, antiguo_nombre, antiguo_precio)
            producto_modificado = True

        if producto_modificado:
            self.db_consulta(query, parametros)  # Ejecutar la consulta
            self.ventana_editar.destroy()  # Cerrar la ventana de edición de productos
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre)
            # Mostrar mensaje para el usuario
            self.get_productos()  # Actualizar la tabla de productos
        else:
            self.ventana_editar.destroy()  # Cerrar la ventana de edición de productos
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado'.format(antiguo_nombre)
            # Mostrar mensaje para el usuario

# Crear la aplicación y ejecutar el bucle principal
if __name__ == "__main__":
    root = tk.Tk()
    app = Producto(root)
    root.mainloop()

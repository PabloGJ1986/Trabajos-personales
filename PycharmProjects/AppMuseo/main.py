import tkinter as tk
from tkinter import LabelFrame, Label, Entry, ttk, W, E, CENTER, Toplevel, Button, StringVar, messagebox
import sqlite3
import random
import string
#Importación de  todas las bibliotecas

# Conectar con la base de datos o crearla si no existe
conn = sqlite3.connect('Trabajadores.db')

# Se crea un cursor para ejecutar consultas SQL
cursor = conn.cursor()

# Creacion de la tabla Empleado en la base de datos Trabajadores
cursor.execute('''
   CREATE TABLE IF NOT EXISTS Empleado (
       Nombre TEXT,
       Apellidos TEXT,
       DNI TEXT,
       Puesto TEXT,
       Contraseña TEXT
   )
''')

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()
#Se define la clase Empleado
class Empleado:
   def __init__(self, root):#Se define el método de inicialización (__init__) para la clase
       self.ventana = root
       self.ventana.title("App de Museo") #Se establece el título de la ventana principal como "App de Museo".
       self.ventana.resizable(1, 1) #Metodo que hace la ventana redimensionable
       # en ambas direcciones (ancho y alto)
       self.ventana.iconbitmap("C:\\Users\\gymja\\Downloads\\museum_3584.ico")
       #Icono de la ventana principal utilizando un archivo de icono localizado esa ruta
       # Cambiar el color de fondo de la ventana principal
       self.ventana.configure(bg='#E0E0E0')

       self.crear_ventana_inicio_sesion() # Iniciar sesión

   def db_consulta(self, consulta, parametros=()):
       try:# Intentar establecer una conexión con la base de datos llamada 'Trabajadores.db'
           with sqlite3.connect('Trabajadores.db') as con:# Creacion de  un cursor para ejecutar comandos SQL en la conexión
               cursor = con.cursor()
               cursor.execute(consulta, parametros)
               # Se ejecuta la consulta SQL con los parámetros proporcionados y
               #confirmacion de cambios en la base de datos
               con.commit()
               return cursor.fetchall() # Mostrar todos los resultados de la consulta
       except sqlite3.Error as e: #Si lo anterior no es posible
           #se devuleve la posible excepción de SQLite y muestra un mensaje de error
           print(f"Error en la conexión a la base de datos: {e}")
           return [] # lista vacía en caso de error

   def limpiar_campos_ventana_principal(self):
       # Limpiar los campos de entrada en la ventana principal
       self.ventana_editar.destroy()
   def get_Empleados(self): #En esta funcion se bbtiene los registros actuales en la tabla (si existen)
       registros_tabla = self.tabla.get_children()
       for fila in registros_tabla:# Se eliminan todas las filas actuales de la tabla
       #Antes de realizar una consulta en la base de datos
           self.tabla.delete(fila)

       # Consulta SQL para ordenar por Nombre en orden ascendente
       query = 'SELECT Nombre, Apellidos, DNI, Puesto, Contraseña FROM Empleado ORDER BY Nombre ASC'
       # Realizar una consulta a la base de datos y obtener los registros necesarios
       registros_db = self.db_consulta(query)

       # Se itera sobre los registros obtenidos de la base de datos con bucle for
       for fila in registros_db:
           # Donde la fila tenga al menos 5 elementos
           if len(fila) >= 5:
               # Y el primer elemento se utiliza como identificador (iid) en el Treeview
               iid = fila[0]

               # Se verifica si el iid no está en los registros actuales de la tabla
               if iid not in self.tabla.get_children():
                   # Añadir una nueva fila en el Treeview con los valores de la base de datos
                   self.tabla.insert('', 'end', iid=iid, values=(fila[0], fila[1], fila[2], fila[3], fila[4]))

   def generar_contraseña(self, longitud=12):#Metodo para generar y mostrar una contraseña
       #aletaria con esa longitud como maximo
       caracteres = string.ascii_letters + string.digits + string.punctuation
       #Caracteristicas de esa contraseña(letras,mayusculas y minusculas,digitos y caracteres de puntuación)
       contraseña_generada = ''.join(random.choice(caracteres) for _ in range(longitud))
       return contraseña_generada #Devuelve la contraseña generada
   def mostrar_datos(self): #Metodo para mostrar unos datos de la base de datos y tabla Empleado
       try:
           query = 'SELECT * FROM Empleado'
           registros_db = self.db_consulta(query)

           print("Registros obtenidos:", registros_db)#Imprime los registros obtenidos de la base de datos.

           if registros_db: #Si hay registros en la base de datos,mostrar por pantalla
               print("Datos de la base de datos:")
               for fila in registros_db:
                   print(fila)
           else: #Si no hay registros, imprimir un mensaje indicando que no hay datos
               print("No hay datos en la base de datos.")

           #Actualizacion en la interfaz de usuario con datos de empleados de la base de datos
           self.get_Empleados()
       except Exception as e: #Imprimir cualquier excepcion ocurrida durante el proceso y mostrar
           #un mensaje de error
           print(f"Error al mostrar datos: {e}")

   def crear_ventana_inicio_sesion(self):
       #Metodo para crear una ventana de inicio de sesión
       self.ventana_login = Toplevel(self.ventana)
       # Configuracion del título de la ventana de inicio de sesión
       self.ventana_login.title("Inicio de Sesión")
       self.ventana_login.iconbitmap("C:\\Users\\gymja\\Downloads\\museum_3584.ico")
       #Icono de la ventana de inicio de sesión

       # Etiqueta y campo de entrada para el nombre de usuario
       tk.Label(self.ventana_login, text="Nombre de usuario:", font=("Arial", 12)).grid(row=0, column=0,
                                                                                            pady=10, padx=10,
                                                                                            sticky="e")
       self.entry_usuario = Entry(self.ventana_login, font=("Arial", 12))
       self.entry_usuario.grid(row=0, column=1, pady=10, padx=10)

       tk.Label(self.ventana_login, text="Contraseña:", font=("Arial", 12)).grid(row=1, column=0, pady=10,
                                                                                     padx=10,
                                                                                     sticky="e")
       self.entry_contraseña = Entry(self.ventana_login, show="*", font=("Arial", 12))
       #SHOW "*" configura para el atributo no sea visible y se reemplaza por *
       self.entry_contraseña.grid(row=1, column=1, pady=10, padx=10)
       #Row,column y sus numeros son su fila,pady y padx su espacio vertical y horizontal,respectivamente
       # Botón para iniciar sesión con el comando de verificación de credenciales
       btn_iniciar_sesion = Button(self.ventana_login, text="Iniciar Sesión", command=self.verificar_credenciales,
                                   font=("Arial", 12)) #Fuente empleada y tamaño
       btn_iniciar_sesion.grid(row=2, columnspan=2, pady=10)

   def verificar_credenciales(self):
       # Obtener el nombre de usuario y la contraseña introducida por el usuario
       usuario_ingresado = self.entry_usuario.get()
       contraseña_ingresada = self.entry_contraseña.get()

       # Definir las credenciales de administrador
       ADMIN_USER = "DireccionMuseo"
       ADMIN_PASSWORD = "Pablo"

       # Comprobar si las credenciales coinciden con las del administrador
       if usuario_ingresado == ADMIN_USER and contraseña_ingresada == ADMIN_PASSWORD:
           self.mostrar_mensaje_exitoso("Inicio de Sesión administrador", "¡Bienvenido, Administrador!")
           self.ventana_login.destroy()
           self.iniciar_app()
       else:
           # Mostrar mensaje de error si la autenticación no es correcta
           self.mostrar_mensaje_error("Error", "Credenciales incorrectas. Por favor, inténtelo de nuevo.")

   def mostrar_mensaje_exitoso(self, titulo, mensaje):
       messagebox.showinfo(titulo, mensaje)

   def mostrar_mensaje_error(self, titulo, mensaje):
       messagebox.showerror(titulo, mensaje)
  #Metodos que se llaman desde la funcion principal verificar_credenciales para dar un mensaje exitoso o de error
   def iniciar_app(self):

       frame = LabelFrame(self.ventana, text="Añadir nuevo empleado", font=("Arial", 15, "bold"))
       frame.grid(row=0, column=0, columnspan=3, pady=20)
       #Se crea un marco (LabelFrame) llamado ("Añadir nuevo empleado") para organizar los wigdet con esas
       #caracteristicas de tamaño y columnas.
       self.nombre_var = StringVar(value='')
       self.apellidos_var = StringVar(value='')
       self.Dni_var = StringVar(value='')
       self.Puesto_var = StringVar(value='')
       self.Contraseña_var = StringVar(value='')
      #Se crean variables de control (StringVar) para almacenar valores de los campos de entrada
       #y modificar y acceder a los valores.
       self.create_label_entry(frame, "Nombre: ", row=1, textvariable=self.nombre_var)
       self.create_label_entry(frame, "Apellidos: ", row=2, textvariable=self.apellidos_var)
       self.create_label_entry(frame, "DNI: ", row=3, textvariable=self.Dni_var)
       self.create_label_entry(frame, "Puesto: ", row=4, textvariable=self.Puesto_var)
       self.create_label_entry(frame, "Contraseña: ", row=5, textvariable=self.Contraseña_var, readonly=True)
      #con la funcion Create_label_entry se crean campos y etiquetas de entrada en el marco.
       self.boton_aniadir = ttk.Button(frame, text="Guardar Empleado", command=self.guardar_empleado)
       self.boton_aniadir.grid(row=6, columnspan=2, sticky='w' + 'e')
    #Se crea un botón para guardar el empleado con sus caracteristicas
       self.mensaje = Label(text='', fg='red')
       self.mensaje.grid(row=7, column=0, columnspan=2, sticky=W + E)
     #Creacion una etiqueta para mostrar mensajes (actualmente en rojo)
       style = ttk.Style()
       style.configure("MyStyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
       style.configure("MyStyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
       style.layout("MyStyle.Treeview", [('MyStyle.Treeview.treearea', {'sticky': 'nswe'})])
    #Configuracion de estilos para Treeview (tabla) y sus encabezados
       self.tabla = ttk.Treeview(height=20, columns=(1, 2, 3, 4, 5), style="MyStyle.Treeview")
       #Creacion Widget Treeview con 5 columnas,fila 8 y columnas de 0 a 1.
       self.tabla.grid(row=8, column=0, columnspan=2)

       # Configuración de encabezados
       self.tabla.heading('#1', text='Nombre', anchor=CENTER)
       self.tabla.heading('#2', text='Apellidos', anchor=CENTER)
       self.tabla.heading('#3', text='DNI', anchor=CENTER)
       self.tabla.heading('#4', text='Puesto', anchor=CENTER)
       self.tabla.heading('#5', text='Contraseña', anchor=CENTER)
       # Configuración de columnas
       self.tabla.column('#1', width=150, minwidth=150, anchor=CENTER)
       self.tabla.column('#2', width=150, minwidth=150, anchor=CENTER)
       self.tabla.column('#3', width=150, minwidth=150, anchor=CENTER)
       self.tabla.column('#4', width=150, minwidth=150, anchor=CENTER)
       self.tabla.column('#5', width=150, minwidth=150, anchor=CENTER)

       self.get_Empleados() #Se carga inicialmente a los datos de Empleados en la Tabla

       self.boton_eliminar = ttk.Button(text='ELIMINAR', command=self.eliminar_empleado)
       self.boton_eliminar.grid(row=6, column=0, sticky=W + E)

       self.boton_editar = ttk.Button(text='EDITAR', command=self.edit_empleado)
       self.boton_editar.grid(row=6, column=1, sticky=W + E)

       self.boton_mostrar_datos = ttk.Button(text='Mostrar Datos', command=self.mostrar_datos)
       self.boton_mostrar_datos.grid(row=9, column=0, columnspan=2, sticky=W + E)
       #Se crean  botones para eliminar,editar y mostrar datos

       self.mostrar_datos()

   def create_label_entry(self, frame, label_text, row, textvariable, readonly=False):
       # Se crea una etiqueta con el texto proporcionado(label_text)
       etiqueta = Label(frame, text=label_text)
       # Colocacion de la etiqueta en la fila especificada y en la primera columna del marco
       etiqueta.grid(row=row, column=0, sticky=E)

       # Crear un campo de entrada (Entry) vinculado a una variable de control (textvariable)
       # El estado del campo de entrada es "readonly" si readonly es True,sino se establece como "normal"
       entry = Entry(frame, textvariable=textvariable, state="readonly" if readonly else "normal")
       # Colocacion del campo de entrada en la misma fila y la segunda columna del marco
       entry.grid(row=row, column=1)

       # Devolver el campo de entrada recién creado
       return entry

   def guardar_empleado(self):
       #Funcion donde se obtienen los valores actuales de las variables de control
       nombre = self.nombre_var.get()
       apellidos = self.apellidos_var.get()
       dni = self.Dni_var.get()
       puesto = self.Puesto_var.get()
       contraseña = self.Contraseña_var.get()

       # Comprobacion que los campos obligatorios están completos
       if nombre and apellidos and dni and puesto:
           # Generacion de una contraseña automáticamente antes de guardar el empleado
           contraseña_generada = self.generar_contraseña()
           self.Contraseña_var.set(contraseña_generada)

           # Creacion de  la consulta SQL para insertar un nuevo empleado en la base de datos
           query = 'INSERT INTO Empleado (Nombre, Apellidos, DNI, Puesto, Contraseña) VALUES (?, ?, ?, ?, ?)'
           parametros = (nombre, apellidos, dni, puesto, contraseña_generada)

           # Ejecutar la consulta SQL sus parametros
           self.db_consulta(query, parametros)

           # Actualizar la tabla de empleados en la interfaz gráfica del usuario
           self.get_Empleados()


           # Limpiar los campos de entrada y establecer un mensaje de que el empleado fue creado correctamente
           self.nombre_var.set('')
           self.apellidos_var.set('')
           self.Dni_var.set('')
           self.Puesto_var.set('')
           self.Contraseña_var.set('')
           self.mensaje['text'] = 'Empleado guardado correctamente'
       else:
           # Sino poner un mensaje de error si algún campo obligatorio está vacío
           self.mensaje['text'] = 'Todos los campos son obligatorios'

   def eliminar_empleado(self):

       self.mensaje['text'] = ''# Limpiar el mensaje de la interfaz

       try:
           #Se obteiene la fila actualmente seleccionada en el Treeview
           seleccion = self.tabla.focus()

    # o en caso contrario comprobar si se ha seleccionado una fila y recordar que seleccione un empleado
           if not seleccion:
               raise IndexError("Por favor, seleccione un empleado")

           # Obtener el DNI directamente de la fila seleccionada en el Treeview
           dni = self.tabla.item(seleccion, 'values')[2]

           # Eliminar el empleado de la base de datos utilizando el DNI y registrar la hora de eliminación
           query = 'DELETE FROM Empleado WHERE DNI = ?'
           parametros = (dni,)
           self.db_consulta(query, parametros)

           # Mostrar  información de la eliminacion del empleado y su dni en Base de Datos
           print(f"Empleado con DNI {dni} eliminado de la base de datos")

           # Eliminar directamente la fila seleccionada del Treeview
           self.tabla.delete(seleccion)

           # # Mostrar  información de la eliminacion
           print(f"Empleado con DNI {dni} eliminado del Treeview")

           # Establecer un mensaje de éxito en la interfaz del usuario
           self.mensaje['text'] = f'Empleado con DNI {dni} eliminado con éxito'

       except Exception as e:
           # En caso de producirse ,mostrar mensaje de error en la interfaz
           self.mensaje['text'] = f"Error al eliminar el empleado: {e}"

   def edit_empleado(self):
       # Limpiar el mensaje de la interfaz del usuario
       self.mensaje['text'] = ''  # Mensaje inicialmente vacío

       try:
           # Obtener las filas seleccionadas en el Treeview
           seleccion = self.tabla.selection()

           # Verificar si se ha seleccionado alguna fila y mostrar un mensaje de aviso
           if not seleccion:
               raise IndexError("Por favor, seleccione un empleado")

           # Obtener los valores actuales del empleado seleccionado
           old_empleado = self.tabla.item(seleccion, 'values')

           # Crear una nueva ventana para editar el empleado
           self.ventana_editar = Toplevel(self.ventana)
           self.ventana_editar.title("Editar Empleado")
           self.ventana_editar.resizable(1, 1)

           # Creacion variables de control para los nuevos valores
           nuevo_nombre_var = StringVar(value=old_empleado[0])
           nuevos_apellidos_var = StringVar(value=old_empleado[1])
           nuevo_dni_var = StringVar(value=old_empleado[2])
           nuevo_puesto_var = StringVar(value=old_empleado[3])
           nuevo_contraseña_var = StringVar(value=old_empleado[4])

           # Creacion campos de entrada en la nueva ventana
           entry_nuevo_nombre = self.create_label_entry(self.ventana_editar, "Nuevo Nombre: ", row=0,
                                                        textvariable=nuevo_nombre_var)
           entry_nuevos_apellidos = self.create_label_entry(self.ventana_editar, "Nuevos Apellidos: ", row=1,
                                                            textvariable=nuevos_apellidos_var)
           entry_nuevo_dni = self.create_label_entry(self.ventana_editar, "Nuevo DNI: ", row=2,
                                                     textvariable=nuevo_dni_var)
           entry_nuevo_puesto = self.create_label_entry(self.ventana_editar, "Nuevo Puesto: ", row=3,
                                                        textvariable=nuevo_puesto_var)
           entry_nuevo_contraseña = self.create_label_entry(self.ventana_editar, "Nueva Contraseña: ",
                                                            row=4,
                                                            textvariable=nuevo_contraseña_var)

           # Creacion botón para aplicar los cambios
           boton_aplicar = Button(self.ventana_editar, text="Aplicar Cambios",
                                  command=lambda: self.aplicar_cambios(
                                      old_empleado[0],
                                      nuevo_nombre_var.get(),
                                      nuevos_apellidos_var.get(),
                                      nuevo_dni_var.get(),
                                      nuevo_puesto_var.get(),
                                      nuevo_contraseña_var.get(),
                                      old_empleado,
                                      entry_nuevo_nombre,
                                      entry_nuevos_apellidos,
                                      entry_nuevo_dni,
                                      entry_nuevo_puesto,
                                      entry_nuevo_contraseña
                                  ))
           boton_aplicar.grid(row=5, columnspan=2)

           # Controlar el evento de cierre de la ventana para limpiar los campos en la ventana principal
           self.ventana_editar.protocol("WM_DELETE_WINDOW", self.limpiar_campos_ventana_principal)

       except IndexError as e:
           # En caso contrario y no seleccionar un empleado, establecer un mensaje de error
           self.mensaje['text'] = str(e)
   def aplicar_cambios(self, old_nombre, nuevo_nombre, nuevos_apellidos, nuevo_dni, nuevo_puesto,
                       nuevo_contraseña, old_empleado,
                       entry_nuevo_nombre, entry_nuevos_apellidos, entry_nuevo_dni, entry_nuevo_puesto,
                       entry_nuevo_contraseña):
       # Verificar que todos los campos requeridos estén rellenos correctamente
       if not (nuevo_nombre and nuevos_apellidos and nuevo_dni and nuevo_puesto and nuevo_contraseña):
           messagebox.showerror("Error", "Todos los campos son obligatorios")
           return

       try:
           # Crear la consulta SQL para actualizar el empleado en la base de datos
           query = 'UPDATE Empleado SET Nombre=?, Apellidos=?, DNI=?, Puesto=?, Contraseña=? WHERE Nombre=?'
           parametros = (nuevo_nombre, nuevos_apellidos, nuevo_dni, nuevo_puesto, nuevo_contraseña, old_nombre)

           # Ejecutar la consulta SQL para actualizar la base de datos
           self.db_consulta(query, parametros)

           # Asegurar los cambios en la base de datos (commit)
           con = sqlite3.connect('Trabajadores.db')
           con.commit()
           con.close()

           # Crear mensajes con los datos antiguos y nuevos para mostrarlos
           antiguos_datos = f"Antiguos datos: Nombre={old_empleado[0]}, Apellidos={old_empleado[1]}, DNI={old_empleado[2]}, Puesto={old_empleado[3]}, Contraseña={old_empleado[4]}"
           nuevos_datos = f"Nuevos datos: Nombre={nuevo_nombre}, Apellidos={nuevos_apellidos}, DNI={nuevo_dni}, Puesto={nuevo_puesto}, Contraseña={nuevo_contraseña}"

           # Imprimir un cuadro de diálogo informativo con los datos antiguos y nuevos
           messagebox.showinfo("Cambios Aplicados", f"{antiguos_datos}\n\n{nuevos_datos}")

           # Actualizar los datos en la interfaz gráfica
           seleccion = self.tabla.selection()
           self.tabla.item(seleccion,
                           values=(nuevo_nombre, nuevos_apellidos, nuevo_dni, nuevo_puesto, nuevo_contraseña))

           # Limpiar los campos de entrada en la ventana de edición
           entry_nuevo_nombre.delete(0, 'end')
           entry_nuevos_apellidos.delete(0, 'end')
           entry_nuevo_dni.delete(0, 'end')
           entry_nuevo_puesto.delete(0, 'end')
           entry_nuevo_contraseña.delete(0, 'end')

           # Cerrar la ventana de edición
           self.ventana_editar.destroy()

       except Exception as e:
           # En caso de error, mostrar un cuadro de error al aplicar esos cambios
           messagebox.showerror("Error", f"Error al aplicar cambios: {e}")

   def mostrar_datos(self):
       try: # Consulta SQL para seleccionar todos los registros de la tabla Empleado
           query = 'SELECT * FROM Empleado'
           registros_db = self.db_consulta(query) # Realizar la consulta en la base de datos

           # Imprimir información de la consulta y los registros obtenidos en la consola
           print("Consulta SQL:", query)
           print("Registros obtenidos:", registros_db)

           # Comprobar si hay registros en la base de datos
           if registros_db:
               print("Datos de la base de datos:")

               # Mostrar cada fila de registros obtenida
               for fila in registros_db:
                   print(fila)
           else:
               print("No hay datos en la base de datos.")

           # Mostrar también los datos en la aplicación actualizando la interfaz gráfica
           self.get_Empleados()
       except Exception as e:
           # En caso de error, imprimir un mensaje de error  al mostrar los datos en la consola
           print(f"Error al mostrar datos: {e}")

if __name__ == '__main__':
    # Iniciar la aplicación cuando se ejecuta el script como un programa independiente
    root = tk.Tk() #Creacion de la ventana principal de la aplicación
    # Definir un estilo para el marco
    estilo = ttk.Style()
    estilo.configure('My.TFrame', background='#FF0000')  # Gris en formato hexadecimal
    root.configure(bg='#FF0000')  # Establece el color de fondo de la ventana principal en gris

    app = Empleado(root) #Crea una instancia de la clase Empleado,que define interfaz
    root.mainloop() #Inicia el bucle principal  de la interfaz gráfica







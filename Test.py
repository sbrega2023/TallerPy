#LIBRERIAS
import pathlib  
import os
import datetime
import logging
import time as TM
import sys
import openpyxl as OPX
import math
import calendar
import FileDialog
from django.utils.translation.trans_real import catalog
from asyncio import streams

#import DataSource

#fichero = FileDialog.FilesDialogs()
#print(fichero.selectFile())

#===============================================================================
# celda = DataSource.DataSource()
# print(celda.xlData())
#===============================================================================

#===============================================================================
# text = 'Filtrar 1 mensajes de advertencia'
# text = text.split()
# 
# print(text, type(text),type(int (text[1])))
#===============================================================================


#===============================================================================
# mitexto = "hola, esto es un textO"
#  
# text = mitexto.split()
# print(text)
# text1 = mitexto.split(',')
# print(text1)
# listaTexto = ['Hola','esto','es','un','texto']
# print(listaTexto)
# cadena = '-'.join(listaTexto)
# print(cadena)
#===============================================================================

#===============================================================================
# def imc(peso , estatura):
#     imc = peso // estatura**2
#     return 
#===============================================================================

#===============================================================================
# peso = float(input('Ingrese Peso en Kg: '))
# estatura = float(input('Ingrese estatura en m: '))
# #print(type(estatura))
# imc = peso // estatura**2 
# print('El imc es: ',imc)
#===============================================================================

#BUCLE FOR
#lista = [5, 2, 4, 3,1]
#lista1 = ['hola', 'esto', 'es un', 'mensaj', 'adios']
#for valorActual in lista:
    #print(valorActual)
    
#for numero in range(5, 10):
#    print(numero)
#===============================================================================
# longitud = len(lista)
# print('la longitud de la lista es: ',longitud)
# for numero in range(len(lista)):
#     print(lista[numero])
#===============================================================================

#===============================================================================
# for palabra in lista1:
#     print('palabra actual: ',palabra)
#     if palabra == 'mensaje':
#         print('Encotre la palabra : ', palabra)
#         break
#===============================================================================
#===============================================================================
# if 'mensaje' in lista1:
#     print('Encontre la palabra buscada')    
#             
# if 'mensaje' not in lista1:
#     print('No Encontre la palabra buscada')  
#===============================================================================

#===============================================================================
# print(lista)
# listaOrdenada = sorted(lista, reverse=True) # tambien se puede ordenar al reves con la palabra reverse=true
# print(listaOrdenada)    
#===============================================================================

#EJERCICIO 4
#===============================================================================
# for numero in sorted(range(100), reverse = True):
#     print(numero)
#===============================================================================
    
#FUNCIONES
#===============================================================================
# def miFuncion():
#     print('mi funcion')
#     for i in range(3):
#         print(i)
# 
# print('antes')
# miFuncion()
# print('despues')
#===============================================================================

#===============================================================================
# def operaciones(a,b):
#     return a + b, a - b, a * b, a / b
#     
# resultado = operaciones(2, 4)
# print(resultado) # obtengo una tupla (6, -2, 8, 0.5)
# print(resultado[0])
#===============================================================================

#===============================================================================
# def anioBisiesto(anio):
#     if calendar.isleap(anio):
#         print('Es año bisiesto')
#     else:
#         print('no es año bisiesto')
# 
# anioBisiesto(2024)
#===============================================================================

#-------------------------------------------------------------------------------------------------
#CLASES Y OBJETOS
#Los objetos son representacion de algo real en la programacion, estan formados por metodos y atributos.

#En Python no existe el concepto de Public, Private, Protected para las clases, son todas publicas, entonces hay una 
#convencion de nombrar a los atributos que no se deberian sobreescribir con un "_" 

#===============================================================================
# class Dino:            # Creamos una clase Dino
#     #Atributos
#     _encendido = True
#      
#     #Metodos
#     def enciende(self):
#         self._encendido = True #Con self. estoy indicando que puedo modifica una variable o atributo del metodo desde afuera
#                                 # sin tocar el Atributo "_encendido"
#          
#     def apaga(self):
#         self._encendido = False 
#      
#     def isEncendido(self):
#         return self._encendido
#      
#  
# d1 = Dino() # Crear un objeto, significa instanciar una clase.
# d1.apaga() #Instaciamos la clase y utilizamos el metodo apaga el cual define la variable _encendido como False
# print(d1._encendido) # aca al haber utilizado self. , vemos que imprime la variable del metodo y no el atributo
#  
# #Creamos otro objeto de la misma clase que no esta relacionado con el primer objeto
# d2 = Dino()
# d2.enciende() # asigno el Valor True
# print(d2.isEncendido()) # imprimo self._encendido con True
# 
# print(d1.isEncendido()) # Aca vemos que las dos instancias creadas son independientes
#===============================================================================

# CLASES ESTATICAS: 
# Comparten un mismo espacio de memoria, las clases dinamicas se instancian 
# y manipulan datos de cada instancia independientemente.

#===============================================================================
# class Estatica:
#     numero = 1
# 
#     def incrementa():
#         Estatica.numero += 1
# 
# Estatica.incrementa()
# print(Estatica.numero)
# Estatica.incrementa()
# print(Estatica.numero)
# Estatica.incrementa()
# print(Estatica.numero)
#===============================================================================

#HERENCIA: consiste en que una clase hereda los atributos y metodos de otra case

#===============================================================================
# class Juguete:            # Creamos una clase Dino
#     #Atributos
#     _encendido = True
#      
#     #Metodos
#     def enciende(self):
#         self._encendido = True #Con self. estoy indicando que puedo modifica una variable o atributo del metodo desde afuera
#                                 # sin tocar el Atributo "_encendido"
#          
#     def apaga(self):
#         self._encendido = False 
#      
#     def isEncendido(self):
#         return self._encendido
# 
# 
# class Potato(Juguete):            # Creamos una clase Dino
#     #Atributos
#        
#     def quitarOreja(self):
#         pass
#     
#     def ponerOreja(self):
#         pass
# 
# 
# class Dino(Juguete):            
#     
#     color = None
#     nombre = None
#         
#     def __init__(self, nombre):  #Constructor sirve para iniciar parametros, solo se dispara cuando instanciamos la clase
#         print("Estoy en el constructor")
#         
#         self.color = "Verde"
#         self.nombre = nombre
#         
#     def verEscamas(self):
#         print("Estoy en la funcion")
#===============================================================================

#p = Potato()
#p.enciende()
#print(p.isEncendido())
#p.apaga()
#print(p.isEncendido())

#===============================================================================
# p = Dino("Seba")
# p1 = Dino("Pani")
# print(p1.verEscamas())
# print(p.color)
# print(p.nombre)
#===============================================================================
# LAS CLASES SON DICCIONARIOS

#CLASES ABSTRACTAS: sirve para deinir un conjunto de metodos comunes a otras clases
#===============================================================================
# from abc import ABC, abstractclassmethod
# class Animal(ABC):
#     @abstractclassmethod # Definimos un metodo como abstracto y tenemos que implementarlo sio si en las clases hijas
#     def sonido(self):
#         pass
#     def diHola(self): # Este metodo no es abstracto y no hace falta implementarlo
#         print("Hola")
# 
# class Perro(Animal): # Aca tengo que si o si implementar el metodo sonido de la clase padre(Animal)
#     def sonido(self):
#         print("Guau")
# 
# class Gato(Animal): # Aca tengo que si o si implementar el metodo sonido de la clase padre(Animal)
#     def sonido(self):
#         print("Miau")
#         
# p = Perro()
# p.sonido()
# p.diHola()
# g = Gato()
# g.sonido()
# g.diHola()
#===============================================================================

#RELACIONES "is a"(es un)son las Herencias(Perro es un Animal, Gato es un Animal) 
            #"has a"(contiene) son las compocisiones donede una clase contiene otra clase

#COMPOCISION: una clase esta compuesta de otras clases.Estas son relaciones "Has a" (Contiene)

#===============================================================================
# class Motor:
#     tipo = "Diesel"
#     
# 
# class Ventanas:
#     cantidad = 5
#     
#     def cambiarCantidad(self,valor):
#         self.cantidad = valor
#     
# class Ruedas:
#     cantidad = 4
# 
# class Carroceria:
#     ventanas = Ventanas()
#     ruedas = Ruedas()
# 
# class Coche:
#     motor = Motor()
#     carroceria = Carroceria()
# 
# c = Coche()
# print("Motor es: ", c.motor.tipo)
# print("Ventana: ",c.carroceria.ventanas.cantidad)
# c.carroceria.ventanas.cambiarCantidad(8)
# print("Ventana: ",c.carroceria.ventanas.cantidad)
#===============================================================================

#Libreria Estandar de Python, buscar en google
#Funciones Built-in
#Programacion MultiHilo
#===============================================================================
# import _thread
# import time
# 
# def horaActual(nombre_thread , tiempo_de_espera):
#     count = 0
#     while count < 5:
#         time.sleep(tiempo_de_espera)
#         count += 1
#         print(f'hilo:{nombre_thread} - {time.ctime(time.time())}')
#         #print('Hola')
# 
# _thread.start_new_thread(horaActual, ('thread_uno', 1))
# _thread.start_new_thread(horaActual, ('thread_dos', 5))
# 
# #Luego para que funcionen los hilos hay que darla tiempo al programa para que se ejecute.
# #Para eso tenemos que bloquear el programa para que se ejecute el programa paralelo y la forma de hacerlo 
# #es usando un While
# print('Los hilos ya se ejecutaron...')
# while True:
#     time.sleep(0.5)
#     #print('tiempo del while')
#===============================================================================

#Funcion logging
#===============================================================================
# import logging
# #Configuro el loguer para que me muestre las severidades segun sus niveles
# logging.basicConfig(level=logging.DEBUG)# info es la severidad mas baja, de ahi muestra todas las demas
# logging.debug('Debug')
# logging.info('info')
# logging.warning('warning')
# logging.error('Error')
# logging.critical('Critical')
#===============================================================================



#Funcion Lambda
#Funcion filter(funcion, lista): aplica una funcion que devuelve True o False a todos los elementos de una lista ,
                # si esa funcion devuelve True guarda ese valor si devuelve False filter no devuelve ese valor-.
#Funcion map(funcion , lista) aplica indiscriminadamente la funcion sobre cada elemento de la lista.
# Funcion reduce(): hay que importar functools
#reduce(funcion, lista): ejecuta de forma recursiva una funcion sobre la lista hasta que la lista se queda con 
# unico elemento.


#Funcion zip(): agrega iterables a una tuppla y los devuelve. Combina listas.
#===============================================================================
# cursos = ['Java','python','git']
# asistentes = [15,20,4]
# demo = zip(cursos,asistentes)
# print(list(demo)) # Resultado es [('Java', 15), ('python', 20), ('git', 4)]
#===============================================================================

#all() y any(): sirven para verificar que todas (all()) las condiciones de una lista se cumplan o algunas(any()) de una lista 
# se cumplan. all seria como una "and" y any seria como un "or"

#===============================================================================
# from functools import reduce
# numeros = [1,2,3,4,5,6,7,8,9]
# #lista = ['Número de Proyecto', 'Tarea del Proyecto','Campo', 'Acción', 'Valor', 'Validación', 'Causa']
# #lista2 = [['Número de Proyecto', None, 'Campo', None, 'Valor', 'Validación', 1],[None,None ,None ,None ,None ,None ,None]]
# def mifuncion(x):
#     #print(x)
#     if x % 2 != 0:
#         return True
#     return False
# resultado = list(filter(mifuncion, numeros))
# print(resultado,type(resultado))
# 
# #res= reduce(lambda a,b : a + b, list(resultado))
# res = reduce(lambda a,b : a+b , resultado)
# print(res,type(res))
# #resultado = filter(any,lista) 
# #print(lista2)
# #print(list(resultado))
#===============================================================================

#Funcion imput() : permite preguntar al usuario por datos
#===============================================================================
# import getpass
# user = input('username: ')
# passwd = input('password: ')
# 
# print(user,passwd)
#===============================================================================
#===============================================================================
# paises = set([input('Ingrese Paises: ')])
# #paises = input('Ingrese Paises: ')
# print(paises,type(paises))
#===============================================================================

#GUIS
# PYGTK , PyQt, wxPython, TKinter,
#(tcl/tk) tcl es un lenguaje de programacion, y tk es un tool kit
#import tkinter
#from test.test_idle import tk
#from dotenv.variables import Variable
#componenetes y widgets :  botones , input, checkbox, todo estos widgets se tiene que poner en un contenedor

#window = tkinter.Tk() #instanciamos la clase Tkinter ,creamos un objeto Windows
#print(type(window))
#Creacion de Widgets: 
#label: sirve para crear una etiqueta
# Creo una etiqueta pero sin mostrar con back ground 'yellow' y fore gorund 'blue'
#label_saludo = tkinter.Label(window,text = 'HOLA!', bg='yellow',fg='blue') 

#Creamos una Geometrias:
#Geometria por Pack:
#label_saludo.pack(ipadx=50,ipady = 50, fill='x')
#label_saludo.pack(ipadx=30,ipady = 30, expand=True)
#label_saludo.pack(ipadx=30,ipady = 30, side='left')

#label_adios = tkinter.Label(window, text = 'Adios!', bg = 'red', fg='white')
#label_adios.pack(ipadx=50,ipady = 100, fill = 'both')
#label_adios.pack(fill = 'both', expand = True)
#label_adios.pack(ipadx=30, ipady=30, side = 'right')

# COMPOSICION
#===============================================================================
# label1 = tkinter.Label(window,text='lable1', bg='yellow',fg='blue')
# label1.pack(ipadx=45,ipady=15)
# 
# label2 = tkinter.Label(window,text='lable2', bg='purple',fg='white')
# label2.pack(ipadx=45,ipady=15, fill='x')
# 
# label3 = tkinter.Label(window,text='lable3', bg='blue',fg='white')
# label3.pack(ipadx=45,ipady=15, fill = 'x')
# 
# label4 = tkinter.Label(window,text='lable4', bg='red',fg='white')
# label4.pack(ipadx=15,ipady=15,side='left')
# 
# label5 = tkinter.Label(window,text='lable5', bg='yellow',fg='black')
# label5.pack(ipadx=15,ipady=15,side='left')
# 
# label6 = tkinter.Label(window,text='lable6', bg='green',fg='black')
# label6.pack(ipadx=15,ipady=15,side='right')
#===============================================================================

#Geomeria mediante GRID (Rejilla , Matriz)
#(0,0) (1,0) (2,0)
#(0,1) (1,1) (2,1)
#(0,2) (1,2) (2,2)
#(0,3) (1,3) (2,3)

#Label Entry (2,0)
#Label Entry (2,1)
#(0,2) (1,2) (2,2)
#(0,3) (1,3) (2,3)

#Configuramos el GRID
#from tkinter import ttk
#from tkinter import Tk
#from tkinter import Message
#window.columnconfigure(0, weight=1)
#window.columnconfigure(0, weight=3)

#===============================================================================
# #Etiqueta Usuario
# username_label = ttk.Label(window, text= 'Username:')
# username_label.grid(column=0, row=0, sticky=tkinter.W, padx=5, pady=5)# stiky (West, East ,) es para fijar la Label, padx y pady es para da
# #Etiqueta Password
# password_label = ttk.Label(window, text= 'Password:')
# password_label.grid(column=0, row=1, sticky=tkinter.W, padx=5, pady=5)# stiky (West, East ,) es para fijar la Label, padx y pady es para da
# 
# #InputBox
# #Campo Usuario
# username_entry = ttk.Entry(window)
# username_entry.grid(column=1, row=0, sticky=tkinter.W, padx=5, pady=5)
# #Campo Password
# password_entry = ttk.Entry(window, show='*')
# password_entry.grid(column=1, row=1, sticky=tkinter.W, padx=5, pady=5)
# 
# #Boton
# login_button = ttk.Button(window, text='Login')
# login_button.grid(column=1, row=3, sticky=tkinter.E, padx=5 , pady=5)
#===============================================================================

#Posicionamiento Absoluto
#===============================================================================
# import random
# colors = ['blue', 'red', 'yellow','purple', 'green','black']
# 
# for x in range(0,10):
#     color = random.randint(0, len(colors)-1)
#     color2 = random.randint(0, len(colors)-1)
#     label = tkinter.Label(window, text='Etiqueta!', bg=colors[color], fg=colors[color2])
#     label.place(x=random.randint(0,100), y=random.randint(0,100))
#===============================================================================

#WIDGET
#1) Frames: se utiliza para agrupar cosas
#===============================================================================
# frame = ttk.Frame(window)
# #print(dir(frame))
# #frame['relief'] = 'sunken' #sunken es un tipo de borde
# label = ttk.Label(frame, text='Hola')
# label.grid(column=0, row=0 ,sticky=tkinter.W, padx=50, pady=50)
# 
# frame.grid(column=0, row=0, sticky=tkinter.W)#Un frame asigna un marco "invisble" para posicionar elementos
#===============================================================================
#2) List box: permite dentro de una serie de elementos seleccionar uno
#===============================================================================
#from tkinter import StringVar
# lista = ['Windows', 'macOS', 'Linux', 'MS DOS', 'AmigaOS', 'OS/2']
# lista_items = StringVar(value=lista)
# listbox = tkinter.Listbox(window, height = 10, listvariable=lista_items)
# listbox.grid(column=0, row=0, sticky=tkinter.W)
#===============================================================================

#RadioButton
#===============================================================================
# def reset(event):
#     print('Reset')
#     seleccionado.set(None)#Limpia las selecciones
#     
#     
# seleccionado = tkinter.StringVar()
# 
# r1 = ttk.Radiobutton(window, text='Si', value='1', variable=seleccionado)
# r2 = ttk.Radiobutton(window, text='No', value='2', variable=seleccionado)
# r3 = ttk.Radiobutton(window, text='Quizá', value='3', variable=seleccionado)
# boton = tkinter.Button(window, text= 'Reinicio')
# 
# r1.grid(column=0,row=1,pady=5,padx=5)
# r2.grid(column=0,row=2,pady=5,padx=5)
# r3.grid(column=0,row=3,pady=5,padx=5)
# boton.grid(column=1,row=4,pady=5,padx=5)
# boton.bind('<Button-1>', reset)
#===============================================================================

 
#seleccionado2 = tkinter.StringVar()
#r1 = ttk.Radiobutton(window, text='Si2', value='12', variable=seleccionado2)
 
#r1.grid(column=1,row=0,pady=5,padx=5)

#CheckBox
#===============================================================================
# def miFuncion():
#     if seleccionado.get() == '1':
#         print('Se han aceptado las condiciones')
#     elif seleccionado2.get() == '1':
#         print('No se han aceptado las condiciones')
#     #print(seleccionado.get(),type(seleccionado.get()))
#     #print(seleccionado.get(),type(seleccionado2.get()))
#     
#         
#         
# seleccionado = tkinter.StringVar()
# seleccionado2 = tkinter.StringVar()
# 
# checkbox = ttk.Checkbutton(window, text='Acepto las condiciones',variable = seleccionado, command = miFuncion)
# 
# checkbox2 = ttk.Checkbutton(window, text='No acepto las condiciones',variable = seleccionado2, command = miFuncion)
# 
# 
# checkbox.grid(row=0, column=0)
# checkbox2.grid(row=1, column=0)
#===============================================================================

#Eventos
#===============================================================================
# def salir(event):
#     print('Salir...')
#     window.quit()
#     
# def saludar(event):
#     print('Has hecho click en saludar...')
# 
# def saludarDobleClick(event):
#     print('Has hecho doble Click en saludar...')
# 
# 
# 
# boton = tkinter.Button(window, text= 'Click')
# boton.pack()
# boton.bind('<Button-1>', saludar)
# boton.bind('<Double-1>', saludarDobleClick)
# 
# botonSalir = tkinter.Button(window, text= 'Salir')
# botonSalir.pack()
# botonSalir.bind('<Button-1>', salir)
#===============================================================================

#===============================================================================
# def motion(event):
#     print('Mouse position: (%s %s)' % (event.x, event.y))
#     return 
# 
# master = Tk()
# texto = "Demo de Texto en un Widget msg para ver el movimiento del raton"
# msg = Message(master, text = texto)
# msg.config(bg='lightgreen', font=('times', 24 , 'italic'))
# msg.bind('<Motion>', motion)
# msg.pack()
#===============================================================================

#Ventanas de Dialago



#Tengo que crear un loop para que me mantenga la ventana (windows) visible.
#window.mainloop()
 
#CAPITULO 11: BASE DE DATOS
#BASE DE DATOS RELACIONALES: son como hojas de calculos (MySQL, MariaDB, Oracle, para proyectos pequeños se usa SQLITE)
# Relacionan unas hojas con otras

#BASE DE DATOS NO RELACIONALES:casandra, influx, 
# requisitos: 
#===============================================================================
# import sqlite3
# import getpass
# from _sqlite3 import connect, Cursor
# from pipenv.vendor.vistir import cursor
# from pandas.tests.io.test_sql import sqlite_buildin
# 
# def verifica_credenciales(username, password):
#     conn = sqlite3.connect('miaplicacion.db')# abre la base de datos con el fichero que vamos a trabajar
#     cursor = conn.cursor()
#     
#     query = f"SELECT id FROM users WHERE username='{username}' AND password='{password}'"
#     print('Query a ejecutar: ', query)
#     
#     rows = cursor.execute(query)
#     print(rows)
#     data = rows.fetchone() #devuelve un solo elemento
#     print(data, type(data))
#     
#     cursor.close()
#     conn.close() # Cerramos la conexión
#     
#     if data == None:
#         return False #Retorna Falso si no encuentra el dato en la tabla
#     return True # True si el dato es encontrado en la tabla
# 
# def crear_usuario(identificador, usuario , clave):
#     conn = sqlite3.connect('miaplicacion.db', isolation_level=None)# abre la base de datos con el fichero que vamos a trabajar
#     cursor = conn.cursor()
#     
#     #querys = 'SELECT * FROM USERS'
#     query = '''INSERT INTO users(id, username , password) VALUES(? ,? ,? )'''
#     
#     #rowss= cursor.execute(querys)
#     rows = cursor.execute(query, (identificador, usuario, clave))
#     print(rows, type(rows))
#     conn.commit()
#     #cursor.execute(query, (identificador, usuario, clave))
#     
#     #===========================================================================
#     # identificador += 1
#     # 
#     # query = '''INSERT INTO users(id, username , password) VALUES(?,?,?)'''
#     # print('Creo usuario2')
#     # cursor.execute(query, (identificador, usuario, clave))
#     # 
#     # conn.commit()
#     #===========================================================================
#     cursor.close()
#     conn.close()
#     
# def main():
#     #crear_usuario(4,'Maria Elena', 'Fusceneco')
#     
#     #-----CREAMOS LA DB 'Colegio.db' y la Tabla alumnos----------
#     conn = sqlite3.connect('Colegio.db', isolation_level=None)# Creamos la DB
#     cursor = conn.cursor()
#     try:
#         conn.execute("""create table alumnos (id integer, Nombre text, Apellido text)""")
#         print("se creo la tabla articulos")                        
#     except sqlite3.OperationalError:
#         print("La tabla Colegio ya existe")                    
#     
#     for i in range(8):
#         id = i
#         nombre = 'Nombre'
#         apellido = 'Apellido'
#         #query = '''INSERT INTO alumnos(id, Nombre , Apellido) VALUES(id ,Nombre ,Apellido )'''
#         #conn.execute =("""INSERT INTO alumnos(id, Nombre , Apellido) VALUES (?,?,?)""")
#         
#         
#         rows = cursor.execute("INSERT INTO alumnos(id, Nombre , Apellido) VALUES (?,?,?)",(id,'Nombre','Apellido'))
#         print(rows, type(rows))
#         conn.commit()
#         
#     cursor.close()
#     conn.close()
# 
#def main2():
#     username = input('Nombre de usuario: ')
#     password = getpass.getpass('Contraseña: ')
#     print(username,password)
#     
#     if verifica_credenciales(username, password):
#         print('Login Correcto')
#     else:
#         print('Log Incorrecto')
#    strn = 'Esto es una cadena'
#    newStrn = strn.replace('e', 'o')
#    print(newStrn,type(newStrn))
# 
#if __name__ == '__main__':
#     print('Main')
#     main2()
#===============================================================================

#INTRODUCCION A DJANGO

#Es un framework, es decir, un conjunto de Herramientas que nos permite desarrllar un sitio web relativamente rapida.
# Para trabajar en un local host hacemos en la consola python manage.py runserver (hay que pararse en el directorio C:\Users\sbrega\eclipse-workspace\miproyectodj\)
# se deben crear aplicaciones que luego deben ser conectadas con el proyecto general.
#Las aplicaciones se pueden crear desde el proyecto -->  Django --> Create application
# Luego para linquear el proyecto gral con la app tengo que ir al archivo setting.py y dentro
#ir a Installer_apps y agregar la app a la lista que en este caso es, catalog.apps.Catalogconfig
# una vez agregada la app tengo que configurar los patrones de las vistas en urlpatterns dentro de urls.py
#dentro del urls.py:
#===============================================================================
#from django.urls import include 
#urlpatterns = [
#     path('admin/', admin.site.urls),
#     #agregamos
#     path('catalog/', include('catalog.urls')),
# ]
#===============================================================================

#Luego tenemos que crear el archivo urls.py en la app catalog y agregamos las siguentes lineas:
#===============================================================================
# import django.urls
# from . import views
# 
# urlpatterns = []
#===============================================================================

#luego ejecutamos el servidor y vemos si funciona.

#luego debo agregar una serie de datos:
#a) ejecutamos python manage.py migrate
#b) verificamos que la db.sqlite3 tiene info
#c) creamos un super usuario , por consola python manage.py createsuperuser
#d) ejecutamos http://127.0.0.1:8000/admin
#b) ejecutamos python manage.py makemigrations (vemos antes que la db.sqlite3 esta en cero)
#c)


#Introduccion a DJANGO

print('hola mundo')
print('hola mundo 2')



























'''
Created on 24 nov. 2022

@author: sbrega
'''
from tkinter import filedialog
#===============================================================================
# askdirectory()
# askopenfile()
# askopenfilename()
# askopenfilenames()
# asksaveasfilename()
# asksaveasfile()
#===============================================================================

# defaultextension: extensión por defecto para guardar determinado archivo.
# filetypes: Indica el tipo de archivo que se pueden abrir.
# initialdir, initialfile; Directorio y archivo inicial.
# title: Cambia el titulo del cuadro de dialogo.

class FilesDialogs():
    global archivo
    def selectFile(self):
        archivo = filedialog.askopenfilename()
        #print(archivo)
        return archivo
        
    def __init__(self):#Inicializacion de variables
        print('Constructor')
        archivo = 'Vacio'
        
#fichero = FilesDialogs()
#print(fichero.selectFile())







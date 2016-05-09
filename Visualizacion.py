#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.



# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 10:33:14 2016

@author: Transito
"""



import sys
from PyQt4 import QtGui, QtCore

import matplotlib.pyplot as plt
import numpy as np

class Window(QtGui.QMainWindow):

    def __init__(self):

#Definicion de la ventana principal donde se alojaran los demas botones y  subventanas
        super(Window, self).__init__()     #Se crea la ventana principal
        self.setGeometry(50, 50, 500, 300) #Se define el tamaño de la ventana principal
        self.setWindowTitle("VISUALIZACIÓN DE ESTRUCTURAS ATÓMICAS EN EL ESPACIO DE CONFIGURACIÓN ESTRUCTURAL")#Se le coloca el nombre de la aplicación a la ventana
        self.setWindowIcon(QtGui.QIcon('C:/Users/Transito/Documents/Python Scripts/icono3.png')) #Se le asigna un icono

#Código Correspondiente a la opcion de editar en donde permite manipuilar y modificar el archivo abierto
#este esl el pop out donde saldrá una vez seleccionada la opción
        openEditor = QtGui.QAction("&Editor", self)#Etiqueta que permite identificar el editor
        openEditor.setShortcut("Ctrl+E")           #Etiqueta de accion rapida de la aplicación
        openEditor.setStatusTip('Abrir el editor')     #Mensaje de la barra de estado de la ventana principal
        openEditor.triggered.connect(self.editor)  #Comando de ejecución del editor



#Código correspondiente al segmento de código en la ventana que permite salir de la aplicación
        extractAction = QtGui.QAction("&Salir de la aplicación", self) #Etiqueta para salir de la aplicación
        extractAction.setShortcut("Ctrl+Q") #Etiqueta de la salida rapida  de la aplicación
        extractAction.setStatusTip('Salir de la aplicación') # Mensaje de la barra de estado de la ventana principal 
        extractAction.triggered.connect(self.close_application)#Comando de ejecución que cierra la aplicción



#Código que permite abrir una ventana y buscar un archivo dentro de lo contenido en el PC que porta la aplicación
#este esl el pop out donde saldrá una vez seleccionada la opción        
        openFile = QtGui.QAction("&Buscar y abrir archivo", self) # Etiqueta que permite identificar la función que permite buscar archivos
        openFile.setShortcut("Ctrl+O")               # Etiqueta de la salida rapida  de la aplicación
        openFile.setStatusTip('Buscar archivo de resulados de calculos realizados con atomos') #Mensaje de la barra de estado de la ventana principal
        openFile.triggered.connect(self.file_open) #Comando de ejecución de abrir ventanas

        self.statusBar()   # Se crea la barra principal en donde se colocará cada las opciones tradicionales, file, editor etc

        mainMenu = self.menuBar() #Se crea la barra de menú y se designa como menú principal
        
        fileMenu = mainMenu.addMenu('&Archivo') #Se crea la función Archivo y a continuación se le asignan las siguientes dos funciones
        fileMenu.addAction(extractAction)#Función de salir y cerrar la aplicación
        fileMenu.addAction(openFile) #Función de abrir archivo
        
        editorMenu = mainMenu.addMenu("&Edición") # Se crea la función de editar 
        editorMenu.addAction(openEditor)    #Se abre un editor normal

        self.home() #Se crea  el espacio interior de la ventana 

#************Creación de los botones que se desean que salgan en la ventana principal**************

    def home(self): #Se definenen los siguientes Botones dentro de la ventana
        global habilita_boton  
#Boton con texto ubicado en cualquier parte de la  ventana que permite salir de la aplicación
        btn = QtGui.QPushButton(QtGui.QIcon('icono_salir.png'),"Salir y Cerrar", self) #Boton  utilizado para salir de la aplicación
        btn.clicked.connect(self.close_application) # Al ser presionado cierra y se sale de la aplicación
        btn.resize(btn.minimumSizeHint())# Se redimenciona el tamaño  del boton a su minimo tamanño
        btn.move(400,250) #Se ubica en la posición especificada
     
#Boton con imagen o icono ubicado en la barra de herramientas        
        extractAction = QtGui.QAction(QtGui.QIcon('icono_salir.png'), 'Salir y Cerrar', self) 
        extractAction.triggered.connect(self.close_application)
        self.toolBar = self.addToolBar("Salir")
        self.toolBar.addAction(extractAction)

#Boton en el menú princilpal, que permite el acceso al cambio de tipo de fuente         
        fontChoice = QtGui.QAction('Fuente', self) #Permite crear la opción de selecciónar el tipo de fuente en la barra principal
        fontChoice.triggered.connect(self.font_choice) #permite abrir la seleeción de tipo de fuente
        #self.toolBar = self.addToolBar("Font") 
        self.toolBar.addAction(fontChoice)      #Permite adicionar el tipo de fuenta a la variable que la selecciona

#Boton en el menú principal que permite el acceso al cambio de tipo de color de fondo de la fuente 
        fontColor = QtGui.QAction('Color fondo fuente', self) #Permite crear el boton que selecciona el tipo de color de fondo de la fuente
        fontColor.triggered.connect(self.color_picker) #Permite abrir la paleta de colores donde se puede seleccionar el color escogido
        self.toolBar.addAction(fontColor)               #Se Almacena el tipo de color de fondo selecionado.

#Boton en el menú principal que permite por medio de una caja de chequeo selecionar el agrandamiento de la ventana principal
        checkBox = QtGui.QCheckBox('Agranda Ventana', self) # Se Crea la caja de chequeo o checkbox
        checkBox.move(200, 250) #Se ubica en cualquier posicion de la ventana principal
        checkBox.stateChanged.connect(self.enlarge_window) #Se modifica las dimenciones de la ventana principal

#Boton en el menú principal que permite por medio de una caja de chequeo selecionar el agrandamiento de la ventana principal
        checkBox = QtGui.QCheckBox('Guardad Datos Prev', self) # Se Crea la caja de chequeo o checkbox
        checkBox.move(120, 65) #Se ubica en cualquier posicion de la ventana principal
        checkBox.stateChanged.connect(self.Habilita_Guardar) #Se modifica las dimenciones de la ventana principal


#Se inserta una barra de progreso que permite mostrar de manera grafica el proceso de trasnformar el sistema de n dimenciones a dos dimenciones
        self.progress = QtGui.QProgressBar(self) #Se crea la barra de progreso
        self.progress.setGeometry(110, 100, 250, 28) #Se le da el tamaño
##****************************************************************************************************


#Boton con texto ubicado en cualquier parte de la  ventana que permite hacer el llamado a la función que realiza el grafico
        btn = QtGui.QPushButton(QtGui.QIcon('icono1.png'),"Archivo Cargar", self) #Boton  utilizado para llamar a graficar la función
        btn.clicked.connect(self.file_open) # Al ser presionado realiza el grafico en otra ventana
        #btn.resize(btn.minimumSizeHint())# Se redimenciona el tamaño  del boton a su minimo tamanño
        btn.move(10,65) #Se ubica en la posición especificada

#Boton con texto ubicado en cualquier parte de la  ventana que permite guardar archivos
        btn = QtGui.QPushButton(QtGui.QIcon('icono3.png'),"Archivo Save", self)        
        btn.clicked.connect(self.file_save) # Al ser presionado realiza el grafico en otra ventana
       #btn.resize(btn.minimumSizeHint())# Se redimenciona el tamaño  del boton a su minimo tamanño
        btn.move(225,65) #Se ubica en la posición especificada
                
        

#Se inserta el Boton que permite activar la barra de progreso  que indica el proceso de trasnformación
        self.btn = QtGui.QPushButton(QtGui.QIcon('icono4.png'),"Transformar",self) # Se crea el boton que activa la barra de progreso
        self.btn.move(10,99)  #Se ubica en cualquier punto de la ventana principal
        self.btn.clicked.connect(self.download) #Se enlaza las activación de la barra de progreso


#Boton con texto ubicado en cualquier parte de la  ventana que permite hacer el llamado a la función que realiza el grafico
        btn = QtGui.QPushButton(QtGui.QIcon('icono2.png'),"Gráficar", self) #Boton  utilizado para llamar a graficar la función
        btn.clicked.connect(self.Grafico_con_matplotlib) # Al ser presionado realiza el grafico en otra ventana
        #btn.resize(btn.minimumSizeHint())# Se redimenciona el tamaño  del boton a su minimo tamanño
        btn.move(10,132) #Se ubica en la posición especificada





#**********************************************************************************

        self.show() # Se termina de mostrar la  ventana
        
#Segmento de código  que permite abrir un archivo y almacenarlo en una variable local
    def file_open(self): # Se crea la función que permite abrir el archivo
        global Archivo_leer        
        name = QtGui.QFileDialog.getOpenFileName(self, 'Abrir y buscar archivo con los resultados entregados por QUANTUM ESPRESSO') #Con el comando se abre la ventana de busqueda y se selecciona el archivo
        #file = open(name,'r') #Se Carga el camino o path del archivo seleccionado en la variable file
        Archivo_leer = open(name,'r') #Se Carga el camino o path del archivo seleccionado en la variable file
        self.busqueda_de_lineas_y_datos()
#        self.editor() #Se crea el editor     
#        with file: #Con el camino o path del archivo cargado en la variable file
#            text = file.read()# Se lee en su totalidad y su contenido se carga en la variable text
#            self.textEdit.setText(text) # Se carga en el editor.


#Segmento de código  que permite abrir un archivo         
    def file_save(self): # Se crea la función que permite guardar el archivo    
         global Archivo_guardar         
         name = QtGui.QFileDialog.getSaveFileName(self, 'Almacenar Archivo') #Con el comando se abre la ventana de busqueda y se selecciona el archivo         
         Archivo_guardar = open(name,'w')



#Segmento de código que permite seleccionar el  color de fondo o background del texto
    def color_picker(self):# Se  crea la función  que permite colocar el color seleccionado
        color = QtGui.QColorDialog.getColor() #Se escoge el color 
        self.styleChoice.setStyleSheet("QWidget { background-color: %s}" % color.name())# Se asigna el color

#Segmento de código que permite  abrir el edior de texto
    def editor(self):#Se crea el editor de texto
        self.textEdit = QtGui.QTextEdit() # Se Carga el texto leido en el editor 
        self.setCentralWidget(self.textEdit) #Se ubica en el centro de la pantalla

#Segmento de código que permite escoger el tipo de letra  a utilizar
    def font_choice(self): # Se crea la seleccion de fuente
        font, valid = QtGui.QFontDialog.getFont() #Se almacena la fuente seleccionado
        if valid:
            self.styleChoice.setFont(font) #Si es una fuente valida se asigna


#Segmento de código que permite ver el incremento en la barra de progreso  desde cero a 100%
    def download(self): #Se crea la función de la animación
        print("Realiza la trasnformación")        
        self.completed = 0 #Se Inicia la variable en 0 %

        while self.completed < 100:  #Ciclo while para completar el llenado
            self.completed += 0.0001
            self.progress.setValue(self.completed)
           

#Segmento de código que permite aumentar de tamaño la ventana principal por medio del check box 

    def enlarge_window(self, state):
        if state == QtCore.Qt.Checked:
            self.setGeometry(50,50,1100, 650)
        else:
            self.setGeometry(50, 50, 500, 300)


#Segmento de código que permite activar el boton de guardar

    def Habilita_Guardar(self, state):
        if state == QtCore.Qt.Checked:
            global habilita_boton 
            global Energias #Variable donde se almacenan las energías
            global Num_Atomos #Variable donde se almacenan el numero de atomos            
            global Energia_Camino             
            print("Atomos: ",Num_Atomos)            
            habilita_boton = 1
            Energias = Energia_Camino.readlines()      
        #print("Energías: ", Energias)  
            
        
        else:
           pass#De otro modo continua dentro de la aplicacion  
        
#Segemento de código que permite salir de la aplicación realizando una pregunta de confirmación por medio de otra ventana
    def close_application(self):
        choice = QtGui.QMessageBox.question(self, 'Saliendo',
                                            "Realmente desea salir de la aplicación?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:  #Si la seleccion es afirmativa
            print("Gracias por usar la aplicación") # ofrece gracias y se sale
            sys.exit()
        else:
            pass#De otro modo continua dentro de la aplicacion      
    
    
    def Grafico_con_matplotlib(self):
        print("Se elabora el grafico interactivo")        
        from matplotlib import cm
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        import numpy as np
        fig = plt.figure("VISUALIZACIÓN DE ESTRUCTURAS ATÓMICAS EN EL ESPACIO DE CONFIGURACIÓN ESTRUCTURAL")
        ax = fig.gca(projection='3d')
        #label = plt.zlabel('Energía en Ry', fontsize=14)        
        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X**2 + Y**(4/2))
        Z = np.sin(R)
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm)
        #%matplotlib qt        
        plt.show()
        
        
        
        
    def busqueda_de_lineas_y_datos(self):
        global Archivo_leer # Variable donde se almacena la ruta donde se encuentra el archivo con los datos
        global Energias #Variable donde se almacenan las energías
        global Num_Atomos #Variable donde se almacenan el numero de atomos
        global Energia_Camino        
        Cadena1 = 'ATOMIC_POSITIONS' #Cadena para filtrar
        Cadena2 = '!    total energy'
        Cadena3 = 'number of atoms/cell      ='
        Cadena4 = 'Final energy'
        indice = 0
        
        #Energia_Camino = 0
        Num_Atomos = 0  
        Cantidad_atomos = 4
        
        Energia_Camino = open('C:/Users/Transito/Documents/Python Scripts/Energias.txt','w') # abre archivo para escribir        
        #print("Despues de  cargado el archivo, se crea el vector columna de la energía se almacena en el archivo Energias ")        
        Posiciones_Atomos = open('C:/Users/Transito/Documents/Python Scripts/Posiciones_Atomos.txt','w') # abre archivo para escribir
        #print("Se crea la matriz de posiciones atomicas y se almacena en el archivo posiciones_Atomos")        
        lineas_Archivo = Archivo_leer.readlines()
        #print(lineas_Archivo)        
        #print("Entró a la función de busqueda_de_lineas_y_datos  y se guardaron en los respectivos registros ")       
        for indice, linea in enumerate(lineas_Archivo):
        #for each_line in lines:
           if Cadena2 in linea:
              print (linea),
              Energia_Camino.write(linea)
          
           if Cadena4 in linea:             
              print (linea),
              Energia_Camino.write(linea)
              
           if Cadena3 in linea:             
              Num_Atomos = linea 
              print (Num_Atomos),    
        
           if Cadena1 in linea:
               for Posiciones_Atomos_Raw in lineas_Archivo[indice+1:indice+(Cantidad_atomos + 1)]: 
                   #print (Posiciones_Atomos_Raw),
                   Posiciones_Atomos.write(Posiciones_Atomos_Raw)
        
        #Energias = Energia_Camino.read()      
        #print("Energías: ", Energias)  
        #print("Atomos: ", Num_Atomos)
        Energia_Camino.close  # cierra archivo 
        Posiciones_Atomos.close #cierra el archivo







 

def main():
    
    app = QtGui.QApplication(sys.argv)
 #   ex = Example()
    GUI = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()  

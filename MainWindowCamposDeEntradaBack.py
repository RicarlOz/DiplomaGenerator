import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton
from PyQt5 import uic

nombreTaller = 'NA'
fechaTaller = 'NA'

# Clase heredada de QMainWindow (Constructor de ventanas)
class window(QMainWindow):
    def __init__(self):
        # Iniciar el objeto QMainWindow
        QMainWindow.__init__(self)

        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("MainWindowCamposDeEntrada.ui", self)

        # Definir Widgets
        self.lineEditTaller = self.findChild(QLineEdit, "lineEdit_2")
        self.lineEditFecha = self.findChild(QLineEdit, "lineEdit")
        self.pushButtonSaveNext = self.findChild(QPushButton, "pushButton")

        # Evento de Boton
        self.pushButtonSaveNext.clicked.connect(self.clicker)
    
    def clicker(self):
        # Guarda la informacion de taller y su fecha
        nombreTaller = self.lineEditTaller.text()
        fechaTaller = self.lineEditFecha.text()
        print("El nombre del taller es " + nombreTaller + " y su fecha es " + fechaTaller)
        

# Instancia para iniciar una aplicacion
app = QApplication(sys.argv)

# Crear el objeto de la clase
_window = window()

# Mostrar la ventana
_window.show()

# Ejecutar la app
app.exec()
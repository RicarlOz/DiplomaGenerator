import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QPushButton
from PyQt5 import uic

# Clase heredada de QMainWindow (Constructor de ventanas)
class window(QMainWindow):
    def __init__(self):
        # Iniciar el objeto QMainWindow
        QMainWindow.__init__(self)
        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("MainWindowCamposDeEntrada.ui", self)
        

# Instancia para iniciar una aplicacion
app = QApplication(sys.argv)

# Crear el objeto de la clase
_window = window()

# Mostrar la ventana
_window.show()

# Ejecutar la app
app.exec()
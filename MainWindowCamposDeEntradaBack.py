import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

nombreTaller = 'NA'
fechaTaller = 'NA'

# Clase heredada de QMainWindow (Constructor de ventanas)
class window(QMainWindow):
    def __init__(self):
        # Iniciar el objeto QMainWindow
        QMainWindow.__init__(self)
        # super(window, self).__init__()
        self.setFixedSize(800, 600)
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
        widget.setCurrentIndex(widget.currentIndex()+1)

class Ui_Form(QDialog):
    def __init__(self):
        super(Ui_Form, self).__init__()
        uic.loadUi("WidgetCargaDeArchivo.ui", self)
        self.pushButton.clicked.connect(self.pushButton_handler)
        self.pushButton_4.clicked.connect(self.pushButton_handler_4)

    def pushButton_handler(self):
        print("Button pressed")
        self.open_dialog_box()
        
    def open_dialog_box(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        path = filename[0]
        self.label.setText(path)
        print(path)

    def pushButton_handler_4(self):
        print("Button pressed")
        self.open_dialog_box_4()
        
    def open_dialog_box_4(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        path = filename[0]
        self.label_3.setText(path)
        print(path)
        

# Instancia para iniciar una aplicacion
app = QApplication(sys.argv)

widget = QtWidgets.QStackedWidget()

# Crear el objeto de la clase
_window = window()

screen2 = Ui_Form()

widget.addWidget(_window)
widget.addWidget(screen2)

# Mostrar la ventana
# _window.show()
widget.show()

# Ejecutar la app
app.exec()
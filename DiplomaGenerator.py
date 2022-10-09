import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

nombreTaller = 'NA'
fechaTaller = 'NA'
selectedTemplate = None
selectedExcel = None

# Clase heredada de QMainWindow (Constructor de ventanas)
class DiplomaFields(QMainWindow):
    def __init__(self):
        # Iniciar el objeto QMainWindow
        QMainWindow.__init__(self)
        # super(window, self).__init__()
        self.setFixedSize(800, 600)
        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("DiplomaFieldsScreen.ui", self)

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

class FileUpload(QDialog):
    def __init__(self):
        super(FileUpload, self).__init__()
        uic.loadUi("FileUploadScreen.ui", self)
        self.btnChooseFileImg.clicked.connect(self.selectImg)
        self.btnChooseFileExcel.clicked.connect(self.selectExcel)

    def selectImg(self):
        file = QtWidgets.QFileDialog.getOpenFileName()
        path = file[0]
        fileName = path.split('/')[-1]
        self.lbFileNameImg.setText(fileName)
        print(path)

    def selectExcel(self):
        file = QtWidgets.QFileDialog.getOpenFileName()
        path = file[0]
        fileName = path.split('/')[-1]
        self.lbFileNameExcel.setText(fileName)
        print(path)
        

# Instancia para iniciar una aplicacion
app = QApplication(sys.argv)

widget = QtWidgets.QStackedWidget()

# Crear el objeto de la clase
screen1 = DiplomaFields()
screen2 = FileUpload()

widget.addWidget(screen1)
widget.addWidget(screen2)

# Mostrar la ventana
# _window.show()
widget.show()

# Ejecutar la app
app.exec()
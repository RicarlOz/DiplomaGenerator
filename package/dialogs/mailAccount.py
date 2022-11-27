from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit
from PyQt5 import uic

class MailAccount(QDialog):
    def __init__(self):
        super(MailAccount, self).__init__()

        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("package/ui/AccountInformation.ui", self)

        # Definir Widgets
        self.tfMail = self.findChild(QLineEdit, "tfCorreo")
        self.tfClave = self.findChild(QLineEdit, "tfPwd")
        self.btnBack = self.findChild(QPushButton, "btnBack")
        self.btnNext = self.findChild(QPushButton, "btnNext")
        
        
        self.btnBack.clicked.connect(self.goBack)
        self.btnNext.clicked.connect(self.submit)

    # Funcion para definir el orden de las pantallas de acuerdo a la actual
    def setNavigation(self, screenController, previousScreen, nextScreen):
        self.screenController = screenController
        self.previousScreen = previousScreen
        self.nextScreen = nextScreen

    # Funcion para cambiar de pantalla a la que tiene previa
    def goBack(self):
        self.screenController.setCurrentWidget(self.previousScreen)

    # Funcion para guardar acceder a la cuenta de CSOFT de la cual se puedan enviar los correos
    def submit(self):
        global correo, password
        correo = self.tfMail.text()
        password = self.tfClave.text()        
        if correo == '' or password == '':
            correo = 'csoftdiploma@gmail.com'
            password = 'onzqmrumyggsdkak'    

        self.nextScreen.setMail(correo)
        self.nextScreen.setPassword(password)
        self.screenController.setCurrentWidget(self.nextScreen)
from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit
from PyQt5 import uic

class MailAccount(QDialog):
    def __init__(self):
        super(MailAccount, self).__init__()

        uic.loadUi("package/ui/AccountInformation.ui", self)

        self.tfMail = self.findChild(QLineEdit, "tfCorreo")
        self.tfClave = self.findChild(QLineEdit, "tfPwd")
        self.btnBack = self.findChild(QPushButton, "btnBack")
        self.btnNext = self.findChild(QPushButton, "btnNext")
        
        
        self.btnBack.clicked.connect(self.goBack)
        self.btnNext.clicked.connect(self.submit)

    def setNavigation(self, screenController, previousScreen, nextScreen):
        self.screenController = screenController
        self.previousScreen = previousScreen
        self.nextScreen = nextScreen

    def goBack(self):
        self.screenController.setCurrentWidget(self.previousScreen)

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
from PyQt5.QtWidgets import QDialog, QPushButton
from PyQt5 import uic

class SendMailsQuestion(QDialog):
    def __init__(self):
        super(SendMailsQuestion, self).__init__()

        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("package/ui/SendMailsQuestion.ui", self)

        # Definir self.screenControllers
        self.btnYes = self.findChild(QPushButton, "btnYes")
        self.btnNo = self.findChild(QPushButton, "btnNo")
        self.btnBack = self.findChild(QPushButton, "btnBack")

        # Evento de botón
        self.btnBack.clicked.connect(self.goBack)
        self.btnYes.clicked.connect(lambda: self.selectOption(True))
        self.btnNo.clicked.connect(lambda: self.selectOption(False))

    # Funcion para definir el orden de las pantallas de acuerdo a la actual
    def setNavigation(self, screenController, previousScreen, mailScreen, finalScreen):
        self.screenController = screenController
        self.previousScreen = previousScreen
        self.mailScreen = mailScreen
        self.finalScreen = finalScreen

    # Funcion para saber que camino tomar si el usuario decide enviar correos o guardar local y acabar 
    def selectOption(self, sendMail):
        if sendMail:
            self.screenController.setCurrentWidget(self.mailScreen)
        else:
            self.finalScreen.openFolder()
            self.screenController.setCurrentWidget(self.finalScreen)

    # Funcion para cambiar de pantalla a la que tiene previa
    def goBack(self):
        self.previousScreen.reloadPDF()
        self.screenController.setCurrentWidget(self.previousScreen)

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

    def setNavigation(self, screenController, previousScreen, mailScreen, finalScreen):
        self.screenController = screenController
        self.previousScreen = previousScreen
        self.mailScreen = mailScreen
        self.finalScreen = finalScreen

    def selectOption(self, sendMail):
        if sendMail:
            self.screenController.setCurrentWidget(self.mailScreen)
        else:
            self.finalScreen.openFolder()
            self.screenController.setCurrentWidget(self.finalScreen)

    def goBack(self):
        self.previousScreen.reloadPDF()
        self.screenController.setCurrentWidget(self.previousScreen)

from PyQt5.QtWidgets import QDialog, QPushButton, QLabel
from PyQt5 import uic
import os

class FinalScreen(QDialog):
    def __init__(self):
        super(FinalScreen, self).__init__()

        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("package/ui/FinalScreen.ui", self)

        # Definir Widgets
        self.lbPath = self.findChild(QLabel, "lbPath")
        self.btnNext = self.findChild(QPushButton, "btnNext")
        
        self.btnNext.clicked.connect(self.goNext)

    def setDiplomasPath(self, diplomasPath):
        self.diplomasPath = diplomasPath
        self.lbPath.setText(os.getcwd() + diplomasPath)

    def openFolder(self):
        os.startfile(self.diplomasPath)

    def setNavigation(self, screenController, previousScreen, nextScreen):
        self.screenController = screenController
        self.previousScreen = previousScreen
        self.nextScreen = nextScreen

    def goNext(self):
        self.screenController.setCurrentWidget(self.nextScreen)
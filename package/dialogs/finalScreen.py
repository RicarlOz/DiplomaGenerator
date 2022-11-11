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

    def setDiplomasPath(self, diplomasPath):
        self.diplomasPath = diplomasPath
        self.lbPath.setText(os.getcwd() + diplomasPath)

    def openFolder(self):
        os.startfile(self.diplomasPath)

    def setNavigation(self, screenController, previousScreen, nextScreen):
        self.screenController = screenController
        self.previousScreen = previousScreen
        self.nextScreen = nextScreen

    def goBack(self):
        self.screenController.setCurrentWidget(self.previousScreen)

    def goNext(self):
        self.screenController.setCurrentWidget(self.nextScreen)
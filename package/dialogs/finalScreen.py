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
    
    # Funcion para saber donde guardar/crear los diplomas
    def setDiplomasPath(self, diplomasPath):
        self.diplomasPath = diplomasPath
        self.lbPath.setText(os.getcwd() + diplomasPath)

    def openFolder(self):
        os.startfile(self.diplomasPath)

    # Funcion para definir el orden de las pantallas de acuerdo a la actual
    def setNavigation(self, screenController, previousScreen, nextScreen):
        self.screenController = screenController
        self.previousScreen = previousScreen
        self.nextScreen = nextScreen

    # Funcion para cambiar de pantalla a la que tiene delante
    def goNext(self):
        self.screenController.setCurrentWidget(self.nextScreen)
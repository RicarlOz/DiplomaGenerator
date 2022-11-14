from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QTextEdit
from PyQt5 import uic
from package.pdfGenerator import DataAttributes
import pandas as pd

class DiplomaEditFields(QDialog):
    def __init__(self):
        super(DiplomaEditFields, self).__init__()

        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("package/ui/DiplomaEditFieldsScreen.ui", self)

        # Definir Widgets
        self.tfName = self.findChild(QLineEdit, "tfName")
        self.tfDate = self.findChild(QLineEdit, "tfDate")
        self.tfDescription = self.findChild(QTextEdit, "tfDescription")
        self.btnNext = self.findChild(QPushButton, "btnNext")
        self.btnBack = self.findChild(QPushButton, "btnBack")

        # Evento de Boton
        self.btnNext.clicked.connect(self.goNext)
        self.btnBack.clicked.connect(self.goBack)

    def setNavigation(self, screenController, previousScreen, nextScreen):
        self.screenController = screenController
        self.previousScreen = previousScreen
        self.nextScreen = nextScreen

    def setDiplomaData(self, data):
        self.diplomaData = data
        
    def goNext(self):
        
        strEvent = self.tfName.text()
        strDate = self.tfDate.text()
        strDescription = self.tfDescription.toPlainText()

        namesColor = [int(c) for c in self.diplomaData['NombreColor'].split(',')]
        descriptionColor = [int(c) for c in self.diplomaData['DescripcionColor'].split(',')]
        dateColor = [int(c) for c in self.diplomaData['DateColor'].split(',')]

        namesAttributes = DataAttributes('', self.diplomaData['NombreFont'], self.diplomaData['NombreSize'], namesColor)
        descriptionAttributes = DataAttributes(strDescription, self.diplomaData['DescripcionFont'], self.diplomaData['DescripcionSize'], descriptionColor)
        dateAttributes = DataAttributes(strDate, self.diplomaData['DateFont'], self.diplomaData['DateSize'], dateColor)
        
        self.nextScreen.setDiplomaFields(strEvent, namesAttributes, descriptionAttributes, dateAttributes, self.diplomaData['PDFSize'], self.diplomaData['PDFOrientation'])
        self.nextScreen.setImageDesignPath(self.diplomaData['ImageDesign'])
        self.screenController.setCurrentWidget(self.nextScreen)

    def goBack(self):
        self.screenController.setCurrentWidget(self.previousScreen)

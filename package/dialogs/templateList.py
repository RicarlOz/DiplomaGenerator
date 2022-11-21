from PyQt5.QtWidgets import QDialog, QPushButton, QWidget, QVBoxLayout, QScrollArea, QSizePolicy
from PyQt5 import uic, QtCore, QtGui
import pandas as pd

class TemplateList(QDialog):
    def __init__(self):
        super(TemplateList, self).__init__()
        uic.loadUi("package/ui/TemplateList.ui", self)
        self.df = None

        # Definir widgets
        self.btnBack = self.findChild(QPushButton, "btnBack")
        self.scroll = self.findChild(QScrollArea, "scrollArea")
        self.widget = self.findChild(QWidget, "scrollAreaWidgetContents")
        self.vbox = QVBoxLayout()
        self.loadTemplates()

        self.btnBack.clicked.connect(self.goBack)

    # Funcion para definir el orden de las pantallas de acuerdo a la actual
    def setNavigation(self, screenController, previousScreen, nextScreen):
        self.screenController = screenController
        self.previousScreen = previousScreen
        self.nextScreen = nextScreen

    def loadTemplates(self):
        for i in reversed(range(self.vbox.count())): 
            self.vbox.itemAt(i).widget().setParent(None)
        try:
            self.df = pd.read_csv("package/templates/templatesList.csv")

            for _, row in self.df.iterrows():
                button = QPushButton(self.scroll)

                # Size
                sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
                button.setSizePolicy(sizePolicy)
                button.setMinimumSize(QtCore.QSize(250, 60))

                # Font
                font = QtGui.QFont()
                font.setFamily("Yu Gothic UI")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                button.setFont(font)

                # Style
                button.setStyleSheet("border-radius: 10px; background-color: #4361EE")
                button.setText(f"{row['NombreTaller']}\n{row['Fecha']}")

                button.clicked.connect(lambda: self.goNext(row))
                self.vbox.addWidget(button)
        except:
            print('No previous templates.')

        self.widget.setLayout(self.vbox)

    # Funcion para cambiar de pantalla a la que tiene previa
    def goBack(self):
        self.screenController.setCurrentWidget(self.previousScreen)

    # Funcion para cambiar de pantalla a la que tiene delante
    def goNext(self, data):
        self.nextScreen.setDiplomaData(data)
        self.screenController.setCurrentWidget(self.nextScreen)
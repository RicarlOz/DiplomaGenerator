from PyQt5.QtWidgets import QDialog, QPushButton, QWidget, QVBoxLayout, QScrollArea, QSizePolicy
from PyQt5 import uic, QtCore, QtGui
import pandas as pd

class TemplateList(QDialog):
    def __init__(self):
        super(TemplateList, self).__init__()
        uic.loadUi("package/ui/TemplateList.ui", self)

        # Definir widgets
        self.btnBack = self.findChild(QPushButton, "btnBack")
        self.btnNext = self.findChild(QPushButton, "btnNext")
        self.scroll = self.findChild(QScrollArea, "scrollArea")
        self.widget = self.findChild(QWidget, "scrollAreaWidgetContents")
        self.vbox = QVBoxLayout()
        self.loadTemplates()

        self.btnBack.clicked.connect(self.goBack)
        self.btnNext.clicked.connect(self.goNext)

    def setNavigation(self, screenController, previousScreen, nextScreen):
        self.screenController = screenController
        self.previousScreen = previousScreen
        self.nextScreen = nextScreen

    def loadTemplates(self):
        try:
            df = pd.read_csv("package/templates/templatesList.csv")

            for _, row in df.iterrows():
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
                self.vbox.addWidget(button)
        except:
            print('No previous templates.')

        self.widget.setLayout(self.vbox)

    def goBack(self):
        self.screenController.setCurrentWidget(self.previousScreen)

    def goNext(self):
        pass
        # self.screenController.setCurrentWidget(self.previousScreen)
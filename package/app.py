from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QStackedWidget
from PyQt5 import uic
from package.dialogs.diplomaFields import DiplomaFields
from package.dialogs.diplomaDesign import SeleccionTemplate
from package.dialogs.uploadFiles import FileUpload
from package.dialogs.previewPDF import PreviewDiploma
from package.dialogs.sendMailQuestion import SendMailsQuestion
from package.dialogs.mailFields import MailFields
from package.dialogs.mailAccount import MailAccount
from package.dialogs.finalScreen import FinalScreen
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("package/ui/MainWindow.ui", self)

        # Definir Widgets
        self.btnNew = self.findChild(QPushButton, "btnNew")
        self.btnEdit = self.findChild(QPushButton, "btnEdit")
        self.btnExit = self.findChild(QPushButton, "btnExit")

        # Evento de Boton
        self.btnNew.clicked.connect(self.newDiploma)
        self.btnEdit.clicked.connect(self.editDiploma)
        self.btnExit.clicked.connect(self.exit)

    def newDiploma(self):
        screenController.setCurrentWidget(screen1_1)

    def editDiploma(self):
        pass

    def exit(self):
        sys.exit()

# Instancia para iniciar una aplicacion
app = QApplication(sys.argv)
app.setApplicationName('DiplomaGenerator')
app.setApplicationVersion('1.0')

screenController = QStackedWidget()

screen0 = MainWindow()
screen1_1 = DiplomaFields()
screen1_2 = SeleccionTemplate()
screen1_3 = FileUpload()
screen1_4 = PreviewDiploma()
screen1_5 = SendMailsQuestion()
screen1_6 = MailAccount()
screen1_7 = MailFields()
screen1_8 = FinalScreen()

screen1_1.setNavigation(screenController, previousScreen = screen0, nextScreen = screen1_2)
screen1_2.setNavigation(screenController, previousScreen = screen1_1, nextScreen = screen1_3)
screen1_3.setNavigation(screenController, previousScreen = screen1_2, nextScreen = screen1_4, mailScreen = screen1_7, finalScreen = screen1_8)
screen1_4.setNavigation(screenController, previousScreen = screen1_3, nextScreen = screen1_5)
screen1_5.setNavigation(screenController, previousScreen = screen1_4, mailScreen = screen1_6, finalScreen = screen1_7)
screen1_6.setNavigation(screenController, previousScreen = screen1_5, nextScreen = screen1_7)
screen1_7.setNavigation(screenController, previousScreen = screen1_6, nextScreen = screen1_8)
screen1_8.setNavigation(screenController, previousScreen = screen1_5, nextScreen = screen0)

# Main screen
screenController.addWidget(screen0)

# New diploma process
screenController.addWidget(screen1_1)
screenController.addWidget(screen1_2)
screenController.addWidget(screen1_3)
screenController.addWidget(screen1_4)
screenController.addWidget(screen1_5)
screenController.addWidget(screen1_6)
screenController.addWidget(screen1_7)
screenController.addWidget(screen1_8)

# Edit diploma process

screenController.show()

# Ejecutar la app
def run():
    app.exec()
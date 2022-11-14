from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout
from PyQt5 import uic, QtWebEngineWidgets, QtCore
import os

class PreviewDiploma(QDialog):
    def __init__(self):
        super(PreviewDiploma, self).__init__()
        uic.loadUi("package/ui/PreviewDiploma.ui", self)

        # Definir Widgets
        self.btnBack = self.findChild(QPushButton, "btnBack")
        self.btnNext = self.findChild(QPushButton, "btnNext")
        self.pdfLayout = self.findChild(QVBoxLayout, "vlPDF")

        self.pdfViewer = QtWebEngineWidgets.QWebEngineView()
        self.pdfLayout.addWidget(self.pdfViewer)
        self.pdfViewer.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        self.pdfViewer.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.PdfViewerEnabled, True)

        path = os.path.join(os.path.abspath(os.getcwd()), "diplomas.pdf")
        print(path)
        self.pdfViewer.load(QtCore.QUrl.fromUserInput(path))
        self.pdfViewer.reload()

        self.btnBack.clicked.connect(self.goBack)
        self.btnNext.clicked.connect(self.goNext)

    def setNavigation(self, screenController, previousScreen, nextScreen):
        self.screenController = screenController
        self.previousScreen = previousScreen
        self.nextScreen = nextScreen

    def setPreviousScreen(self, screen):
        self.previousScreen = screen

    def reloadPDF(self):
        self.pdfViewer.reload()

    def goBack(self):
        self.screenController.setCurrentWidget(self.previousScreen)

    def goNext(self):
        self.screenController.setCurrentWidget(self.nextScreen)

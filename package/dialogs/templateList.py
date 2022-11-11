from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

class FileUpload(QDialog):
    def __init__(self):
        super(FileUpload, self).__init__()
        uic.loadUi("package/ui/TemplateList.ui", self)


    def setNavigation(self, screenController, previousScreen, nextScreen):
        self.screenController = screenController
        self.previousScreen = previousScreen
        self.nextScreen = nextScreen
    
    def goBack(self):
        self.screenController.setCurrentWidget(self.previousScreen)
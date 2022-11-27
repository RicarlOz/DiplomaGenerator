from PyQt5.QtWidgets import QDialog, QPushButton, QRadioButton, QMessageBox
from PyQt5 import uic

orientation = 'C'
pdfSize = 'Letter'

class SeleccionTemplate(QDialog):
    def __init__(self):
        super(SeleccionTemplate, self).__init__()

        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("package/ui/SeleccionTemplate.ui", self)

        # Definir Widgets
        self.btnLeft = self.findChild(QPushButton, "btnLeft")
        self.btnRight = self.findChild(QPushButton, "btnRight")
        self.btnCenter = self.findChild(QPushButton, "btnCenter")

        self.rbLeft = self.findChild(QRadioButton, "rbLeft")
        self.rbRight = self.findChild(QRadioButton, "rbRight")
        self.rbCenter = self.findChild(QRadioButton, "rbCenter")

        self.btnCarta = self.findChild(QPushButton, "btnCarta")
        self.btnOficio = self.findChild(QPushButton, "btnOficio")
        self.btnA4 = self.findChild(QPushButton, "btnA4")
        self.rbCarta = self.findChild(QRadioButton, "rbCarta")
        self.rbOficio = self.findChild(QRadioButton, "rbOficio")
        self.rbA4 = self.findChild(QRadioButton, "rbA4")

        self.btnNext = self.findChild(QPushButton, "btnNext")
        self.btnBack = self.findChild(QPushButton, "btnBack")

        # Evento de Boton
        self.btnLeft.clicked.connect(lambda: self.selectTemplate('L'))
        self.btnRight.clicked.connect(lambda: self.selectTemplate('R'))
        self.btnCenter.clicked.connect(lambda: self.selectTemplate('C'))

        self.btnCarta.clicked.connect(lambda: self.selectSize('letter'))
        self.btnOficio.clicked.connect(lambda: self.selectSize('legal'))
        self.btnA4.clicked.connect(lambda: self.selectSize('a4'))

        self.btnNext.clicked.connect(self.goNext)
        self.btnBack.clicked.connect(self.goBack)
    
    # Funcion para definir el orden de las pantallas de acuerdo a la actual
    def setNavigation(self, screenController, previousScreen, nextScreen):
        self.screenController = screenController
        self.previousScreen = previousScreen
        self.nextScreen = nextScreen

    # Funcion para pasar valores
    def setDiplomaFields(self, nombreTaller, namesAttributes, descriptionAttributes, dateAttributes):
        self.nombreTaller = nombreTaller
        self.namesAttributes = namesAttributes
        self.descriptionAttributes = descriptionAttributes
        self.dateAttributes = dateAttributes

    # Funcion guardar la posicion en la que muestra la informacion
    def selectTemplate(self, selectedOrientation):
        if selectedOrientation == 'L':
            self.rbLeft.setChecked(True)
        elif selectedOrientation == 'R':
            self.rbRight.setChecked(True)
        else:
            self.rbCenter.setChecked(True)
    
    # Funcion guardar el tamaño del diploma
    def selectSize(self, selectedSize):
        if selectedSize == 'letter':
            self.rbCarta.setChecked(True)
        elif selectedSize == 'legal':
            self.rbOficio.setChecked(True)
        else:
            self.rbA4.setChecked(True)

    # Funcion para cambiar de pantalla a la que tiene previa
    def goBack(self):
        self.screenController.setCurrentWidget(self.previousScreen)
        
    # Funcion para cambiar de pantalla a la que tiene delante
    def goNext(self):
        global orientation, pdfSize

        if not self.rbLeft.isChecked() and not self.rbCenter.isChecked() and not self.rbRight.isChecked():
            QMessageBox.warning(self, "Orientación no seleccionada.", "Selecciona la orientación del diploma para continuar.")
            return
        
        if not self.rbA4.isChecked() and not self.rbCarta.isChecked() and not self.rbOficio.isChecked():
            QMessageBox.warning(self, "Tamaño no seleccionado.", "Selecciona el tamaño del diploma para continuar.")
            return

        if self.rbLeft.isChecked():
            orientation = 'L'
        elif self.rbCenter.isChecked():
            orientation = 'C'
        else:
            orientation = 'R'

        if self.rbA4.isChecked():
            pdfSize = 'A4'
        elif self.rbCarta.isChecked():
            pdfSize = 'Letter'
        else:
            pdfSize = 'Legal'

        print("Orientation:", orientation)
        print("Size:", pdfSize)
        
        self.nextScreen.setDiplomaFields(self.nombreTaller, self.namesAttributes, self.descriptionAttributes, self.dateAttributes, pdfSize, orientation)
        self.screenController.setCurrentWidget(self.nextScreen)

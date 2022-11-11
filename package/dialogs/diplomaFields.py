from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QTextEdit, QComboBox, QSpinBox, QColorDialog, QMessageBox, QFileDialog
from PyQt5 import uic
from package.pdfGenerator import libraryFonts, DataAttributes
import shutil
import os

nombreTaller = ''

namesAttributes = DataAttributes()
descriptionAttributes = DataAttributes()
dateAttributes = DataAttributes()

class DiplomaFields(QDialog):
    def __init__(self):
        super(DiplomaFields, self).__init__()
        global libraryFonts

        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("package/ui/DiplomaFieldsScreen.ui", self)

        # Definir Widgets
        self.tfName = self.findChild(QLineEdit, "tfName")
        self.tfDate = self.findChild(QLineEdit, "tfDate")
        self.tfDescription = self.findChild(QTextEdit, "tfDescription")
        self.btnNext = self.findChild(QPushButton, "btnNext")
        self.btnBack = self.findChild(QPushButton, "btnBack")

        self.btnColorName = self.findChild(QPushButton, "btnColorName")
        self.cbFontName = self.findChild(QComboBox, "cbFontName")
        self.sbSizeName = self.findChild(QSpinBox, "sbSizeName")

        self.btnColorDesc = self.findChild(QPushButton, "btnColorDesc")
        self.cbFontDesc = self.findChild(QComboBox, "cbFontDesc")
        self.sbSizeDesc = self.findChild(QSpinBox, "sbSizeDesc")

        self.btnColorDate = self.findChild(QPushButton, "btnColorDate")
        self.cbFontDate = self.findChild(QComboBox, "cbFontDate")
        self.sbSizeDate = self.findChild(QSpinBox, "sbSizeDate")

        self.btnAddFont = self.findChild(QPushButton, "btnAddFont")
        self.availableFonts = libraryFonts.copy()

        if not os.path.exists("package/fonts/"):
            os.makedirs("package/fonts/")
        
        for font in os.listdir("package/fonts"):
            if font[-4:] == ".ttf":
                self.availableFonts.append(font[:-4])

        self.availableFonts.sort()
        self.cbFontName.addItems(self.availableFonts)
        self.cbFontDesc.addItems(self.availableFonts)
        self.cbFontDate.addItems(self.availableFonts)

        # Evento de Boton
        self.btnColorName.clicked.connect(lambda: self.selectColor("Name"))
        self.btnColorDesc.clicked.connect(lambda: self.selectColor("Desc"))
        self.btnColorDate.clicked.connect(lambda: self.selectColor("Date"))
        self.sbSizeName.valueChanged.connect(lambda: self.sizeChange("Name"))
        self.sbSizeDesc.valueChanged.connect(lambda: self.sizeChange("Desc"))
        self.sbSizeDate.valueChanged.connect(lambda: self.sizeChange("Date"))
        self.btnAddFont.clicked.connect(self.addFont)

        self.btnNext.clicked.connect(self.submit)
        self.btnBack.clicked.connect(self.goBack)

    def setNavigation(self, screenController, previousScreen, nextScreen):
        self.screenController = screenController
        self.previousScreen = previousScreen
        self.nextScreen = nextScreen

    def sizeChange(self, type):
        global namesAttributes, descriptionAttributes, dateAttributes
        if type == "Name":
            namesAttributes.size = self.sbSizeName.value()
        if type == "Desc":
            descriptionAttributes.size = self.sbSizeDesc.value()
        if type == "Date":
            dateAttributes.size = self.sbSizeDate.value()

    def selectColor(self, type):
        global namesAttributes, descriptionAttributes, dateAttributes
        fontColor = QColorDialog.getColor()

        if fontColor.isValid() and type=="Name":
            namesAttributes.color = fontColor.getRgb()
            self.btnColorName.setStyleSheet(f'''background-color: rgb({namesAttributes.color[0]}, {namesAttributes.color[1]}, {namesAttributes.color[2]}); border-radius: 10px;''')
        if fontColor.isValid() and type=="Desc":
            descriptionAttributes.color = fontColor.getRgb()
            self.btnColorDesc.setStyleSheet(f'''background-color: rgb({descriptionAttributes.color[0]}, {descriptionAttributes.color[1]}, {descriptionAttributes.color[2]}); border-radius: 10px;''')
        if fontColor.isValid() and type=="Date":
            dateAttributes.color = fontColor.getRgb()
            self.btnColorDate.setStyleSheet(f'''background-color: rgb({dateAttributes.color[0]}, {dateAttributes.color[1]}, {dateAttributes.color[2]}); border-radius: 10px;''')

    def addFont(self):
        file = QFileDialog.getOpenFileName(filter="*.ttf")
        path = file[0]
        file_extension = os.path.splitext(path)[1]

        if path == "":
            print("File not chosen.")
            return

        if file_extension not in [".ttf"]:
            QMessageBox.warning(self, "Archivo no soportado", "Los archivos soportados son: .ttf")
            return

        fileName = path.split('/')[-1]

        if not os.path.isfile("./fonts/" + fileName):
            shutil.copy(path, "./fonts/")

            self.availableFonts.append(fileName[:-4])
            self.availableFonts.sort()

            # Reaload combobox
            self.cbFontName.clear()
            self.cbFontDesc.clear()
            self.cbFontDate.clear()
            self.cbFontName.addItems(self.availableFonts)
            self.cbFontDesc.addItems(self.availableFonts)
            self.cbFontDate.addItems(self.availableFonts)

        self.cbFontName.setCurrentIndex(self.availableFonts.index(fileName[:-4]))
        self.cbFontDesc.setCurrentIndex(self.availableFonts.index(fileName[:-4]))
        self.cbFontDate.setCurrentIndex(self.availableFonts.index(fileName[:-4]))
    
    def submit(self):
        global namesAttributes, descriptionAttributes, dateAttributes, nombreTaller

        # Guarda la informacion de taller y su fecha
        namesAttributes.font = self.cbFontName.currentText()
        descriptionAttributes.font = self.cbFontDesc.currentText()
        dateAttributes.font = self.cbFontDate.currentText()
        
        nombreTaller = self.tfName.text()
        dateAttributes.text = self.tfDate.text()
        descriptionAttributes.text = self.tfDescription.toPlainText()
        
        self.nextScreen.setDiplomaFields(nombreTaller, namesAttributes, descriptionAttributes, dateAttributes)
        self.screenController.setCurrentWidget(self.nextScreen)

    def goBack(self):
        self.screenController.setCurrentWidget(self.previousScreen)

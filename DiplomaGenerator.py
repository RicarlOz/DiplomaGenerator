from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWebEngineWidgets, QtCore
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator, QValidator
from PyQt5.QtCore import QRegExp
from fpdf import FPDF
import pandas as pd
import os
import sys
import pprint
import shutil
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

correo = 'csoftdiplomagendev@gmail.com'
password = ''
nombreTaller = None
fechaTaller = None
diplomaDescription = None
asuntoCorreo = None
cuerpoCorreo = None
templateDesign = None
selectedImage = None
selectedData = None
templateSize = None
nombreSize = 18
descriptionSize = 14
fechaSize = 14
df = None
libraryFonts = ['Arial', 'Courier', 'Helvetica', 'Symbol', 'Times', 'ZapfDingbats']
screens = []
nameMailList =[]
nameList = []
testMails = ['csoftdiplomagendev@gmail.com', 'csoftdiplomagendev@gmail.com', 'csoftdiplomagendev@gmail.com', 'csoftdiplomagendev@gmail.com']
diplomasPath = None

selectedFont = None
fontColorEvento = (0, 0, 0, 1)
fontColorDesc = (0, 0, 0, 1)
fontColorDate = (0, 0, 0, 1)
sbSizeEvento = 12
sbSizeDesc = 12
sbSizeDate = 12

class DiplomaFields(QDialog):
    def __init__(self):
        super(DiplomaFields, self).__init__()
        global libraryFonts

        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("ui/DiplomaFieldsScreen.ui", self)

        # Definir Widgets
        self.tfName = self.findChild(QLineEdit, "tfName")
        self.tfDate = self.findChild(QLineEdit, "tfDate")
        self.btnSubmit = self.findChild(QPushButton, "btnSubmit")
        self.tfDescription = self.findChild(QTextEdit, "tfDescription")

        self.btnColorEvento = self.findChild(QPushButton, "btnColorEvento")
        self.cbFontEvento = self.findChild(QComboBox, "cbFontEvento")
        self.sbSizeEvento = self.findChild(QSpinBox, "sbSizeEvento")

        self.btnColorDesc = self.findChild(QPushButton, "btnColorDesc")
        self.cbFontDesc = self.findChild(QComboBox, "cbFontDesc")
        self.sbSizeDesc = self.findChild(QSpinBox, "sbSizeDesc")

        self.btnColorDate = self.findChild(QPushButton, "btnColorDate")
        self.cbFontDate = self.findChild(QComboBox, "cbFontDate")
        self.sbSizeDate = self.findChild(QSpinBox, "sbSizeDate")
        

        self.btnAddFont = self.findChild(QPushButton, "btnAddFont")
        self.availableFonts = libraryFonts

        if not os.path.exists("./fonts/"):
            os.makedirs("./fonts/")
        
        for font in os.listdir("./fonts"):
            if font[-4:] == ".ttf":
                self.availableFonts.append(font[:-4])

        self.availableFonts.sort()
        self.cbFontEvento.addItems(self.availableFonts)
        self.cbFontDesc.addItems(self.availableFonts)
        self.cbFontDate.addItems(self.availableFonts)

        # Evento de Boton
        self.btnSubmit.clicked.connect(self.submit)
        self.btnColorEvento.clicked.connect(lambda: self.selectColor("Evento"))
        self.btnColorDesc.clicked.connect(lambda: self.selectColor("Desc"))
        self.btnColorDate.clicked.connect(lambda: self.selectColor("Date"))
        self.sbSizeEvento.valueChanged.connect(lambda: self.sizeChange("Evento"))
        self.sbSizeDesc.valueChanged.connect(lambda: self.sizeChange("Desc"))
        self.sbSizeDate.valueChanged.connect(lambda: self.sizeChange("Date"))
        self.btnAddFont.clicked.connect(self.addFont)

    def sizeChange(self, type):
        global sbSizeEvento, sbSizeDesc, sbSizeDate
        if type == "Evento":
            sbSizeEvento = self.sbSizeEvento.value()
        if type == "Desc":
            sbSizeDesc = self.sbSizeDesc.value()
        if type == "Date":
            sbSizeDate = self.sbSizeDate.value()

    def selectColor(self, type):
        global fontColor, fontColorEvento, fontColorDesc, fontColorDate
        fontColor = QColorDialog.getColor()

        if fontColor.isValid() and type=="Evento":
            fontColorEvento = fontColor.getRgb()
            self.btnColorEvento.setStyleSheet(f'''background-color: rgb({fontColorEvento[0]}, {fontColorEvento[1]}, {fontColorEvento[2]}); border-radius: 10px;''')
        if fontColor.isValid() and type=="Desc":
            fontColorDesc = fontColor.getRgb()
            self.btnColorDesc.setStyleSheet(f'''background-color: rgb({fontColorDesc[0]}, {fontColorDesc[1]}, {fontColorDesc[2]}); border-radius: 10px;''')
        if fontColor.isValid() and type=="Date":
            fontColorDate = fontColor.getRgb()
            self.btnColorDate.setStyleSheet(f'''background-color: rgb({fontColorDate[0]}, {fontColorDate[1]}, {fontColorDate[2]}); border-radius: 10px;''')

    def addFont(self):
        global selectedFont, avaliab

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
            self.cbFontEvento.clear()
            self.cbFontDesc.clear()
            self.cbFontDate.clear()
            self.cbFontEvento.addItems(self.availableFonts)
            self.cbFontDesc.addItems(self.availableFonts)
            self.cbFontDate.addItems(self.availableFonts)

        self.cbFontEvento.setCurrentIndex(self.availableFonts.index(fileName[:-4]))
        self.cbFontDesc.setCurrentIndex(self.availableFonts.index(fileName[:-4]))
        self.cbFontDate.setCurrentIndex(self.availableFonts.index(fileName[:-4]))
    
    def submit(self):
        global diplomaDescription, fechaTaller, nombreTaller, selectedFontEvento, selectedFontDesc, selectedFontDate
        # Guarda la informacion de taller y su fecha
        selectedFontEvento = self.cbFontEvento.currentText()
        selectedFontDesc = self.cbFontDesc.currentText()
        selectedFontDate = self.cbFontDate.currentText()
        nombreTaller = self.tfName.text()
        fechaTaller = self.tfDate.text()
        diplomaDescription = self.tfDescription.toPlainText()

        # if nombreTaller == '' or fechaTaller == '' or diplomaDescription == '':
        #     QMessageBox.warning(self, "Campos restantes.", "Llena la información de los campos para continuar.")
        #     return

        print("El nombre del taller es " + nombreTaller + "la descripcion es " + diplomaDescription + "y su fecha es " + fechaTaller)
        print("El font elegido para el diploma es: " + selectedFontEvento)
        widget.setCurrentIndex(widget.currentIndex()+1)

class SeleccionTemplate(QDialog):
    def __init__(self):
        super(SeleccionTemplate, self).__init__()

        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("ui/SeleccionTemplate.ui", self)

        # Definir Widgets
        self.btnLeft = self.findChild(QPushButton, "btnLeft")
        self.btnRight = self.findChild(QPushButton, "btnRight")
        self.btnCenter = self.findChild(QPushButton, "btnCenter")
        self.rbLeft = self.findChild(QRadioButton, "rbLeft")
        self.rbRight = self.findChild(QRadioButton, "rbRight")
        self.rbCenter = self.findChild(QRadioButton, "rbCenter")
        self.btnNext = self.findChild(QPushButton, "btnNext")
        self.btnBack = self.findChild(QPushButton, "btnBack")
        self.btnCarta = self.findChild(QPushButton, "btnCarta")
        self.btnOficio = self.findChild(QPushButton, "btnOficio")
        self.btnA4 = self.findChild(QPushButton, "btnA4")
        self.rbCarta = self.findChild(QRadioButton, "rbCarta")
        self.rbOficio = self.findChild(QRadioButton, "rbOficio")
        self.rbA4 = self.findChild(QRadioButton, "rbA4")

        # Evento de Boton
        self.btnLeft.clicked.connect(lambda: self.selectTemplate('L'))
        self.btnRight.clicked.connect(lambda: self.selectTemplate('R'))
        self.btnCenter.clicked.connect(lambda: self.selectTemplate('C'))
        self.btnCarta.clicked.connect(lambda: self.selectSize('letter'))
        self.btnOficio.clicked.connect(lambda: self.selectSize('legal'))
        self.btnA4.clicked.connect(lambda: self.selectSize('a4'))
        self.btnNext.clicked.connect(self.goNext)
        self.btnBack.clicked.connect(self.goBack)

    def selectTemplate(self, templateSelected):
        global templateDesign
        print("Selected:", templateSelected)
        templateDesign = templateSelected
        if templateSelected == 'L':
            self.rbLeft.setChecked(True)
        elif templateSelected == 'R':
            self.rbRight.setChecked(True)
        else:
            self.rbCenter.setChecked(True)
    
    def selectSize(self, sizeSelected):
        global templateSize
        print("Selected:", sizeSelected)
        templateSize = sizeSelected
        if sizeSelected == 'letter':
            self.rbCarta.setChecked(True)
        elif sizeSelected == 'legal':
            self.rbOficio.setChecked(True)
        else:
            self.rbA4.setChecked(True)

    def goBack(self):
        widget.setCurrentIndex(widget.currentIndex()-1)
        
    def goNext(self):
        global templateDesign
        if templateDesign == None:
            QMessageBox.warning(self, "Diseño no seleccionado.", "Selecciona un diseño base para continuar.")
            return
        print("Selected template:", templateDesign)
        widget.setCurrentIndex(widget.currentIndex()+1)

class SeleccionSize(QDialog):
    def __init__(self):
        super(SeleccionSize, self).__init__()

        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("ui/SeleccionSize.ui", self)

        # Definir Widgets
        self.tfNombre = self.findChild(QLineEdit, "tfNombre")
        self.tfDescripcion = self.findChild(QLineEdit, "tfDescripcion")
        self.tfFechas = self.findChild(QLineEdit, "tfFechas")
        self.btnBack = self.findChild(QPushButton, "btnBack")
        self.btnNext = self.findChild(QPushButton, "btnNext")

        # Evento de Boton
        self.btnNext.clicked.connect(self.goNext)
        self.btnBack.clicked.connect(self.goBack)

    def goBack(self):
        print("Back to screen 1")
        widget.setCurrentIndex(widget.currentIndex()-1)

    def goNext(self):
        global templateSize, nombreSize, descriptionSize, fechaSize
        nombreSize = self.tfNombre.text()
        descriptionSize = self.tfDescripcion.text()
        fechaSize = self.tfFechas.text()
        #checar por cuando lo paso a int deja de funcionar
        if templateSize == None:
            QMessageBox.warning(self, "Tamaño del Diploma no seleccionado.", "Selecciona un tamaño de diploma  para continuar.")
            return
        print("Selected size:", templateSize)
        print("Tamaño fuente\nnombre: " + nombreSize + "\ndescripcion: " + descriptionSize + "\nfecha: " + fechaSize)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def validating(self):
        validation_rule = QDoubleValidator(2,150,0)

class FileUpload(QDialog):
    def __init__(self):
        super(FileUpload, self).__init__()
        uic.loadUi("ui/FileUploadScreen.ui", self)
        self.btnChooseFileImg.clicked.connect(self.selectImg)
        self.btnChooseFileExcel.clicked.connect(self.selectExcel)
        self.btnGoBack.clicked.connect(self.goBack)
        self.btnPreviewTemplate.clicked.connect(self.previewTemplate)

    def selectImg(self):
        global selectedImage

        file = QFileDialog.getOpenFileName(filter="*.png *.jpg *.jpeg")
        path = file[0]
        file_extension = os.path.splitext(path)[1]

        if path == "":
            print("File not chosen.")
            return

        if file_extension not in [".png", ".jpg", ".jpeg"]:
            QMessageBox.warning(self, "Archivo no soportado", "Los archivos soportados son: .png, .jpg y .jpeg.")
            return

        selectedImage = path
            
        fileName = path.split('/')[-1]
        self.lbFileNameImg.setText(fileName)
        print(path)

    def selectExcel(self):
        global selectedData, df

        file = QFileDialog.getOpenFileName(filter="*.xlsx *.xls")
        path = file[0]
        file_extension = os.path.splitext(path)[1]

        if path == "":
            print("File not chosen.")
            return

        if file_extension not in [".xlsx", ".xls"]:
            QMessageBox.warning(self, "Archivo no soportado.", "Los archivos soportados son: .xlsx y .xls.")
            return

        selectedData = path

        fileName = path.split('/')[-1]
        self.lbFileNameExcel.setText(fileName)

        if file_extension == ".csv":
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)
            mails = pd.read_excel(path, usecols='B')

        print(path)
        print(df)

        mailList = df.values.tolist()
        for item in mailList:
            nameMailList.append(item)

        for item in nameMailList:
            nameList.append(item[0])

    def goBack(self):
        print("Back to screen 1")
        widget.setCurrentIndex(widget.currentIndex()-1)
        
    def previewTemplate(self):
        global selectedImage, selectedData, screens

        if selectedImage == None or selectedData == None:
            QMessageBox.warning(self, "Archivo no seleccionado.", "Selecciona los archivos para continuar.")
            return
        
        self.createPDF()
        pprint.pprint(widget.children())
        if len(screens) <= 3:
            screen5 = PreviewDiploma()
            screens.append(screen5)
            widget.addWidget(screen5)
        screens[3].reloadPDF()
        widget.setCurrentIndex(widget.currentIndex()+1)

    def createPDF(self):
        global templateDesign, diplomaDescription, fechaTaller, df, selectedFont, fontColor, libraryFonts, diplomasPath, templateSize, nombreSize, descriptionSize, fechaSize
        print(selectedFont)

        #Creates the PDF document
        # pdf = FPDF('L', 'mm', 'Letter')
        pdf = FPDF('L', 'mm', templateSize)

        #Set margins
        pdf.set_margins(left=0, top=0, right=0)

        #Disable auto page break
        pdf.set_auto_page_break(False)

        #Add a page
        pdf.add_page()

        #Add font
        if not selectedFontEvento in libraryFonts:
            pdf.add_font(selectedFontEvento, "", './fonts/' + selectedFontEvento + '.ttf', True)
        
        if not selectedFontDesc in libraryFonts:
            pdf.add_font(selectedFontDesc, "", './fonts/' + selectedFontDesc + '.ttf', True)

        if not selectedFontDate in libraryFonts:
            pdf.add_font(selectedFontDate, "", './fonts/' + selectedFontDate + '.ttf', True)

        #Set font color
        #pdf.set_text_color(fontColor[0], fontColor[1], fontColor[2])

        now = datetime.now()

        ##### Individual Diploma #####

        dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")

        if nombreTaller in ['', None]:
            diplomasPath = os.path.join(os.path.abspath(os.getcwd()), "Diplomas\\Evento " + dt_string + '\\')
        else:
            diplomasPath = os.path.join(os.path.abspath(os.getcwd()), "Diplomas\\" + nombreTaller + '\\')

        print('==================================')
        print(os.path.abspath(os.getcwd()))
        print(diplomasPath)
        print('==================================')
        
        if not os.path.exists(diplomasPath):
            os.makedirs(diplomasPath)                
        
        ##### Individual Diploma #####

        for idx, row in df.iterrows():
            ##### Individual Diploma #####

            #Creates the PDF document
            pdf_individual = FPDF('L', 'mm', templateSize)
            # pdf_individual = FPDF('L', 'mm', 'Letter')

            #Set margins
            pdf_individual.set_margins(left=0, top=0, right=0)

            #Disable auto page break
            pdf_individual.set_auto_page_break(False)

            #Add a page
            pdf_individual.add_page()

            #Add diploma image
            pdf_individual.image(selectedImage, 0, 0, 279.4, 215.9)
            
            #Set font color
            #pdf_individual.set_text_color(fontColor[0], fontColor[1], fontColor[2])

            ##### Individual Diploma #####

            pdf.image(selectedImage, 0, 0, 279.4, 215.9)

            ## Left
            if templateDesign == 'L':
                pdf.set_font(selectedFontEvento, '', sbSizeEvento)
                pdf.set_text_color(fontColorEvento[0], fontColorEvento[1], fontColorEvento[2])
                pdf.set_xy(24, 82)
                pdf.cell(165, 10, txt=row["Nombre"], border=True, align='L')

                pdf.set_font(selectedFontDesc, '', sbSizeDesc)
                pdf.set_text_color(fontColorDesc[0], fontColorDesc[1], fontColorDesc[2])
                pdf.set_xy(24, 100)
                pdf.multi_cell(165, 5, txt=diplomaDescription, border=True, align='L')

                pdf.set_font(selectedFontDate, '', sbSizeDate)
                pdf.set_text_color(fontColorDate[0], fontColorDate[1], fontColorDate[2])
                pdf.set_xy(24, 150)
                pdf.cell(85, 15, txt=fechaTaller, border=True, align='L')

                ##### Individual Diploma #####

                pdf_individual.set_font(selectedFontEvento, '', sbSizeEvento)
                pdf.set_text_color(fontColorEvento[0], fontColorEvento[1], fontColorEvento[2])
                pdf_individual.set_xy(24, 82)
                pdf_individual.cell(165, 10, txt=row["Nombre"], border=True, align='L')

                pdf_individual.set_font(selectedFontDesc, '', sbSizeDesc)
                pdf.set_text_color(fontColorDesc[0], fontColorDesc[1], fontColorDesc[2])
                pdf_individual.set_xy(24, 100)
                pdf_individual.multi_cell(165, 5, txt=diplomaDescription, border=True, align='L')

                pdf_individual.set_font(selectedFontDate, '', sbSizeDate)
                pdf.set_text_color(fontColorDesc[0], fontColorDesc[1], fontColorDesc[2])
                pdf_individual.set_xy(24, 150)
                pdf_individual.cell(85, 15, txt=fechaTaller, border=True, align='L')

                ##### Individual Diploma #####
                
            ## Right
            elif templateDesign == 'R':
                pdf.set_font(selectedFontEvento, '', sbSizeEvento)
                pdf.set_text_color(fontColorEvento[0], fontColorEvento[1], fontColorEvento[2])
                pdf.set_xy(92 - 25, 82)
                pdf.cell(165, 10, txt=row["Nombre"], border=True, align='R')

                pdf.set_font(selectedFontDesc, '', sbSizeDesc)
                pdf.set_text_color(fontColorDesc[0], fontColorDesc[1], fontColorDesc[2])
                pdf.set_xy(92 - 25, 100)
                pdf.multi_cell(165, 5, txt=diplomaDescription, border=True, align='R')

                pdf.set_font(selectedFontDate, '', sbSizeDate)
                pdf.set_text_color(fontColorDate[0], fontColorDate[1], fontColorDate[2])
                pdf.set_xy(172 - 25, 150)
                pdf.cell(85, 15, txt=fechaTaller, border=True, align='R')

                ##### Individual Diploma #####

                pdf_individual.set_font(selectedFontEvento, '', sbSizeEvento)
                pdf.set_text_color(fontColorEvento[0], fontColorEvento[1], fontColorEvento[2])
                pdf_individual.set_xy(92 - 25, 82)
                pdf_individual.cell(165, 10, txt=row["Nombre"], border=True, align='R')

                pdf_individual.set_font(selectedFontDesc, '', sbSizeDesc)
                pdf.set_text_color(fontColorDesc[0], fontColorDesc[1], fontColorDesc[2])
                pdf_individual.set_xy(92 - 25, 100)
                pdf_individual.multi_cell(165, 5, txt=diplomaDescription, border=True, align='R')

                pdf_individual.set_font(selectedFontDate, '', sbSizeDate)
                pdf.set_text_color(fontColorDate[0], fontColorDate[1], fontColorDate[2])
                pdf_individual.set_xy(172 - 25, 150)
                pdf_individual.cell(85, 15, txt=fechaTaller, border=True, align='R')

                ##### Individual Diploma #####

            ## Center
            else:
                width = 170
                pdf.set_font(selectedFontEvento, '', sbSizeEvento)
                pdf.set_text_color(fontColorEvento[0], fontColorEvento[1], fontColorEvento[2])
                pdf.set_xy((279.4 / 2 - width / 2) + 10, 120)
                pdf.cell(width, 10, txt=row["Nombre"], border=False, align='C')

                pdf.set_font(selectedFontDesc, '', sbSizeDesc)
                pdf.set_text_color(fontColorDesc[0], fontColorDesc[1], fontColorDesc[2])
                pdf.set_xy((279.4 / 2 - width / 2) + 10, 135)
                pdf.multi_cell(width, 5, txt=diplomaDescription, border=False, align='C')

                pdf.set_font(selectedFontDate, '', sbSizeDate)
                pdf.set_text_color(fontColorDate[0], fontColorDate[1], fontColorDate[2])
                pdf.set_xy(180, 195)
                pdf.cell(85, 15, txt=fechaTaller, border=False, align='C')

                ##### Individual Diploma #####

                pdf_individual.set_font(selectedFontEvento, '', sbSizeEvento)
                pdf.set_text_color(fontColorEvento[0], fontColorEvento[1], fontColorEvento[2])
                pdf_individual.set_xy((279.4 / 2 - width / 2) + 10, 120)
                pdf_individual.cell(width, 10, txt=row["Nombre"], border=False, align='C')

                pdf_individual.set_font(selectedFontDesc, '', sbSizeDesc)
                pdf.set_text_color(fontColorDesc[0], fontColorDesc[1], fontColorDesc[2])
                pdf_individual.set_xy((279.4 / 2 - width / 2) + 10, 135)
                pdf_individual.multi_cell(width, 5, txt=diplomaDescription, border=False, align='C')

                pdf_individual.set_font(selectedFontDate, '', sbSizeDate)
                pdf.set_text_color(fontColorDate[0], fontColorDate[1], fontColorDate[2])
                pdf_individual.set_xy(180, 195)
                pdf_individual.cell(85, 15, txt=fechaTaller, border=False, align='C')
                ##### Individual Diploma #####
            
            if idx < len(df) - 1:
                pdf.add_page()
            
            ##### Individual Diploma #####

            pdf_individual.output(diplomasPath + row["Nombre"] + ' - ' + nombreTaller + '.pdf')
            del pdf_individual

            ##### Individual Diploma #####

        pdf.output("diplomas.pdf")
        del pdf

class PreviewDiploma(QDialog):
    def __init__(self):
        super(PreviewDiploma, self).__init__()
        uic.loadUi("ui/PreviewDiploma.ui", self)

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

    def reloadPDF(self):
        self.pdfViewer.reload()

    def goBack(self):
        print("Back to screen 1")
        pprint.pprint(widget.children())
        widget.setCurrentIndex(widget.currentIndex()-1)

    def goNext(self):
        print(len(screens))
        if len(screens) <= 4:
            screen5 = SendMailsQuestion()
            screens.append(screen5)
            widget.addWidget(screen5)
        widget.setCurrentIndex(widget.currentIndex()+1)

class SendMailsQuestion(QDialog):
    def __init__(self):
        super(SendMailsQuestion, self).__init__()

        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("ui/SendMailsQuestion.ui", self)

        # Definir Widgets
        self.btnYes = self.findChild(QPushButton, "btnYes")
        self.btnNo = self.findChild(QPushButton, "btnNo")
        self.btnBack = self.findChild(QPushButton, "btnBack")

        # Evento de botón
        self.btnBack.clicked.connect(self.goBack)
        self.btnYes.clicked.connect(lambda: self.selectOption(True))
        self.btnNo.clicked.connect(lambda: self.selectOption(False))

    def selectOption(self, sendMail):
        if sendMail:
            if len(widget.children()) <= 6:
                screen6 = MailFields()
                widget.addWidget(screen6)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            if len(widget.children()) <= 6:
                screen7 = FinalScreen()
                widget.addWidget(screen7)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def goBack(self):
        screens[3].reloadPDF()
        widget.setCurrentIndex(widget.currentIndex()-1)

class MailFields(QDialog):
    def __init__(self):
        super(MailFields, self).__init__()

        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("ui/MailFields.ui", self)

        # Definir Widgets
        self.btnBack = self.findChild(QPushButton, "btnBack")
        self.btnNext = self.findChild(QPushButton, "btnNext")
        self.tfAsunto = self.findChild(QLineEdit, "tfName")
        self.tfContenido = self.findChild(QTextEdit, "tfDescription")

        # Evento de botón
        self.btnBack.clicked.connect(self.goBack)
        self.btnNext.clicked.connect(self.submit)
        
    def goBack(self):
        widget.setCurrentIndex(widget.currentIndex()-1)
    
    def submit(self):
        asuntoCorreo = self.tfAsunto.text()
        cuerpoCorreo = self.tfContenido.toPlainText()
        i = 0
        while i < len(nameList):
            message = MIMEMultipart()
            message['From'] = correo
            message.attach(MIMEText(cuerpoCorreo, 'html'))
            print(nameList)
            print(i)
            subj = asuntoCorreo + nameList[i]
            message['Subject'] = subj
            print(message['Subject'])
            message['To'] = testMails[i]
            #The body and the attachments for the mail
            pdfFilePath = diplomasPath + nameList[i] + ' - ' + nombreTaller + '.pdf'
            print(pdfFilePath)
            attach_file_name = pdfFilePath
            attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
            payload = MIMEBase('application', 'octate-stream')
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload) #encode the attachment
            #add payload header with filename
            payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
            message.attach(payload)
            #Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
            session.starttls() #enable security
            session.login(correo, password) #login with mail_id and password
            text = message.as_string()
            #print(correo, testMails[i], text)
            session.sendmail(correo, testMails[i], text)
            session.quit()
            print('Mail Sent')
            del message
            i+=1
        if len(widget.children()) <= 7:
                screen7 = FinalScreen()
                widget.addWidget(screen7)
        widget.setCurrentIndex(widget.currentIndex()+1)

class FinalScreen(QDialog):
    def __init__(self):
        super(FinalScreen, self).__init__()

        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("ui/FinalScreen.ui", self)

        # Definir Widgets
        self.lbPath = self.findChild(QLabel, "lbPath")

        self.lbPath.setText(os.getcwd() + diplomasPath)

        os.startfile(diplomasPath)

# Instancia para iniciar una aplicacion
app = QApplication(sys.argv)

widget = QStackedWidget()

# Crear el objeto de la clase
screen1 = DiplomaFields()
screen2 = SeleccionTemplate()
screen3 = FileUpload()

screens.append(screen1)
screens.append(screen2)
screens.append(screen3)

for screen in screens:
    widget.addWidget(screen)

# Mostrar la ventana
# _window.show()
widget.show()

# Ejecutar la app
app.exec()
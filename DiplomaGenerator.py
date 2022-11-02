from PyQt5.QtWidgets import QApplication, QDialog, QRadioButton, QMessageBox, QFileDialog, QStackedWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QFontComboBox
from PyQt5 import uic, QtWebEngineWidgets, QtCore
from fpdf import FPDF
# import PIL.Image as Image
import pandas as pd
import os
import sys
import time

nombreTaller = 'NA'
fechaTaller = 'NA'
asuntoCorreo = 'NA'
cuerpoCorreo = 'NA'
diplomaDescription = ''
templateDesign = None
selectedImage = None
df = None

class DiplomaFields(QDialog):
    def __init__(self):
        super(DiplomaFields, self).__init__()

        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("DiplomaFieldsScreen.ui", self)

        # Definir Widgets
        self.tfName = self.findChild(QLineEdit, "tfName")
        self.tfDate = self.findChild(QLineEdit, "tfDate")
        self.btnSubmit = self.findChild(QPushButton, "btnSubmit")
        self.tfDescription = self.findChild(QTextEdit, "tfDescription")

        # Evento de Boton
        self.btnSubmit.clicked.connect(self.submit)
    
    def submit(self):
        # Guarda la informacion de taller y su fecha
        nombreTaller = self.tfName.text()
        fechaTaller = self.tfDate.text()
        diplomaDescription = self.tfDescription.toPlainText()
        print("El nombre del taller es " + nombreTaller + " la descripcion es " + diplomaDescription + " y su fecha es " + fechaTaller)
        widget.setCurrentIndex(widget.currentIndex()+1)

class SeleccionTemplate(QDialog):
    def __init__(self):
        super(SeleccionTemplate, self).__init__()

        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("SeleccionTemplate.ui", self)

        # Definir Widgets
        self.btnLeft = self.findChild(QPushButton, "btnLeft")
        self.btnRight = self.findChild(QPushButton, "btnRight")
        self.btnCenter = self.findChild(QPushButton, "btnCenter")
        self.rbLeft = self.findChild(QRadioButton, "rbLeft")
        self.rbRight = self.findChild(QRadioButton, "rbRight")
        self.rbCenter = self.findChild(QRadioButton, "rbCenter")
        self.btnNext = self.findChild(QPushButton, "btnNext")
        self.btnBack = self.findChild(QPushButton, "btnBack")
        self.btnColor = self.findChild(QPushButton, "btnColor")
        self.fontBox = self.findChild(QFontComboBox, "fontBox" )

        # Evento de Boton
        self.btnLeft.clicked.connect(lambda: self.selectTemplate('L'))
        self.btnRight.clicked.connect(lambda: self.selectTemplate('R'))
        self.btnCenter.clicked.connect(lambda: self.selectTemplate('C'))
        # self.rbLeft.toggled.connect(lambda: self.selectTemplate('L'))
        # self.rbRight.toggled.connect(lambda: self.selectTemplate('R'))
        # self.rbCenter.toggled.connect(lambda: self.selectTemplate('C'))
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

    def goBack(self):
        widget.setCurrentIndex(widget.currentIndex()-1)
        
    def goNext(self):
        global templateDesign, fontText
        fontText = self.fontBox.currentText()
        if templateDesign == None:
            QMessageBox.warning(self, "Diseño no seleccionado.", "Selecciona un diseño base para continuar.")
            return
        print("Selected template:", templateDesign)
        print("El font elegido para el diploma es: " + fontText)
        widget.setCurrentIndex(widget.currentIndex()+1)

class FileUpload(QDialog):
    def __init__(self):
        super(FileUpload, self).__init__()
        uic.loadUi("FileUploadScreen.ui", self)
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
        global df

        file = QFileDialog.getOpenFileName(filter="*.xlsx *.xls *.csv")
        path = file[0]
        file_extension = os.path.splitext(path)[1]

        if path == "":
            print("File not chosen.")
            return

        if file_extension not in [".xlsx", ".xls", ".csv"]:
            QMessageBox.warning(self, "Archivo no soportado.", "Los archivos soportados son: .xlsx, .xls y .csv.")
            return

        fileName = path.split('/')[-1]
        self.lbFileNameExcel.setText(fileName)

        if file_extension == ".csv":
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)

        print(path)
        print(df)

    def goBack(self):
        print("Back to screen 1")
        widget.setCurrentIndex(widget.currentIndex()-1)
        
    def previewTemplate(self):
        self.createPDF()
        widget.setCurrentIndex(widget.currentIndex()+1)

    def createPDF(self):
        global templateDesign, diplomaDescription, fechaTaller, df, fontText

        #Creates the PDF document
        pdf = FPDF('L', 'mm', 'Letter')

        #Set margins
        pdf.set_margins(left=0, top=0, right=0)

        #Disable auto page break
        pdf.set_auto_page_break(False)

        #Add a page
        pdf.add_page()

        #Add font
        # pdf.add_font(fontText, "", 'C:\Windows\Fonts')

        for idx, row in df.iterrows():
            pdf.image(selectedImage, 0, 0, 279.4, 215.9)

            ## Left
            if templateDesign == 'L':
                pdf.set_font(fontText, 'B', 18)
                pdf.set_xy(24, 82)
                pdf.cell(165, 10, txt=row["Nombre"], border=True, align='L')

                pdf.set_font(fontText, '', 14)
                pdf.set_xy(24, 100)
                pdf.multi_cell(165, 5, txt=diplomaDescription, border=True, align='L')

                pdf.set_font(fontText, '', 14)
                pdf.set_xy(24, 150)
                pdf.cell(85, 15, txt=fechaTaller, border=True, align='L')
                
            ## Right
            elif templateDesign == 'R':
                pdf.set_font(fontText, 'B', 25)
                pdf.set_text_color(241, 194, 50)
                pdf.set_xy(92 - 25, 82)
                pdf.cell(165, 10, txt=row["Nombre"], border=True, align='R')

                pdf.set_font(fontText, '', 14)
                pdf.set_text_color(255, 255, 255)
                pdf.set_xy(92 - 25, 100)
                pdf.multi_cell(165, 5, txt=diplomaDescription, border=True, align='R')

                pdf.set_font(fontText, '', 14)
                pdf.set_text_color(255, 255, 255)
                pdf.set_xy(172 - 25, 150)
                pdf.cell(85, 15, txt=fechaTaller, border=True, align='R')

            ## Center
            else:
                width = 170
                pdf.set_font(fontText, 'B', 18)
                pdf.set_xy((279.4 / 2 - width / 2) + 10, 120)
                pdf.cell(width, 10, txt=row["Nombre"], border=False, align='C')

                pdf.set_font(fontText, '', 14)
                pdf.set_xy((279.4 / 2 - width / 2) + 10, 135)
                pdf.multi_cell(width, 5, txt=diplomaDescription, border=False, align='C')

                pdf.set_font(fontText, '', 14)
                pdf.set_xy(180, 195)
                pdf.cell(85, 15, txt=fechaTaller, border=False, align='C')
            
            if idx < len(df) - 1:
                pdf.add_page()

        pdf.output("diplomas.pdf")

class PreviewDiploma(QDialog):
    def __init__(self):
        super(PreviewDiploma, self).__init__()
        uic.loadUi("PreviewDiploma.ui", self)

        # Definir Widgets
        self.btnBack = self.findChild(QPushButton, "btnBack")
        self.btnNext = self.findChild(QPushButton, "btnNext")
        self.pdfLayout = self.findChild(QVBoxLayout, "vlPDF")

        pdfViewer = QtWebEngineWidgets.QWebEngineView()
        self.pdfLayout.addWidget(pdfViewer)
        # pdfViewer.setGeometry()
        pdfViewer.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        pdfViewer.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.PdfViewerEnabled, True)

        path = os.path.join(os.path.abspath(os.getcwd()), "diplomas.pdf")
        print(path)
        pdfViewer.load(QtCore.QUrl.fromUserInput(path))
        pdfViewer.reload()

        self.btnBack.clicked.connect(self.goBack)
        self.btnNext.clicked.connect(self.sendMail)


    def goBack(self):
        print("Back to screen 1")
        widget.setCurrentIndex(widget.currentIndex()-1)

    def sendMail(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

##tfName, tfDescription, btnSubmit
class SendMail(QDialog):
    def __init__(self):
        super(SendMail, self).__init__()
        uic.loadUi("EmailScreen.ui", self)

        self.tfAsunto = self.findChild(QLineEdit, "tfSubject")
        self.tfContenido = self.findChild(QTextEdit, "tfBody")
        self.btnSubmit = self.findChild(QPushButton, "btnSubmit")

        self.btnSubmit.clicked.connect(self.submit)

    def submit(self):
        asuntoCorreo = self.tfAsunto.text()
        cuerpoCorreo = self.tfContenido.toPlainText()
        print("El asunto del correo es: " + asuntoCorreo + " el contenido del correo es: " + cuerpoCorreo)
        print("Mostrar siguiente pantalla")
        # widget.setCurrentIndex(widget.currentIndex()+1)




# Instancia para iniciar una aplicacion
app = QApplication(sys.argv)

widget = QStackedWidget()

# Crear el objeto de la clase
screen1 = DiplomaFields()
screen2 = SeleccionTemplate()
screen3 = FileUpload()
screen4 = PreviewDiploma()
screen5 = SendMail()

widget.addWidget(screen1)
widget.addWidget(screen2)
widget.addWidget(screen3)
widget.addWidget(screen4)
widget.addWidget(screen5)

# Mostrar la ventana
# _window.show()
widget.show()

# Ejecutar la app
app.exec()
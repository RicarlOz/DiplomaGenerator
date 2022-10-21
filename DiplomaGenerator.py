from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QFileDialog, QStackedWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit
from PyQt5 import uic, QtWebEngineWidgets, QtCore
from fpdf import FPDF
# import PIL.Image as Image
import pandas as pd
import os
import sys
import time

nombreTaller = 'NA'
fechaTaller = 'NA'
selectedTemplate = None
df = None


# Clase heredada de QMainWindow (Constructor de ventanas)
class DiplomaFields(QDialog):
    def __init__(self):
        super(DiplomaFields, self).__init__()

        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("DiplomaFieldsScreen.ui", self)

        # Definir Widgets
        self.tfName = self.findChild(QLineEdit, "tfName")
        self.tfDate = self.findChild(QLineEdit, "tfDate")
        self.btnSubmit = self.findChild(QPushButton, "btnSubmit")

        # Evento de Boton
        self.btnSubmit.clicked.connect(self.submit)
    
    def submit(self):
        # Guarda la informacion de taller y su fecha
        nombreTaller = self.tfName.text()
        fechaTaller = self.tfDate.text()
        descripcion = self.txtDescripcion.toPlainText()
        print("El nombre del taller es " + nombreTaller + "la descripcion es " + descripcion + "y su fecha es " + fechaTaller)
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
        file = QFileDialog.getOpenFileName()
        path = file[0]
        file_extension = os.path.splitext(path)[1]

        if path == "":
            print("File not chosen.")
            return

        if file_extension not in [".png", ".jpg", ".jpeg"]:
            QMessageBox.warning(self, "Archivo no soportado", "Los archivos soportados son: .png, .jpg y .jpeg.")
            return
            
        fileName = path.split('/')[-1]
        self.lbFileNameImg.setText(fileName)
        print(path)

    def selectExcel(self):
        global df

        file = QFileDialog.getOpenFileName()
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
        if len(widget.children()) <= 3:
            screen3 = PreviewDiploma()
            widget.addWidget(screen3)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def createPDF(self):
        #Creates the PDF document
        pdf = FPDF('L', 'mm', 'Letter')

        #Set margins
        pdf.set_margins(left=0, top=0, right=0)

        #Add a page
        pdf.add_page()

        pdf.image("Design/design1.jpg", 0, 0, 279.4, 215.9)

        pdf.set_xy(22, 76)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(165, 10, txt="RICARDO SERGIO GOMEZ CARDENAS", border=True, align='L')

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

    def goBack(self):
        print("Back to screen 1")
        widget.setCurrentIndex(widget.currentIndex()-1)


# Instancia para iniciar una aplicacion
app = QApplication(sys.argv)

widget = QStackedWidget()

# Crear el objeto de la clase
screen1 = DiplomaFields()
screen2 = FileUpload()

widget.addWidget(screen1)
widget.addWidget(screen2)

# Mostrar la ventana
# _window.show()
widget.show()

# Ejecutar la app
app.exec()
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt5 import uic
from package.pdfGenerator import previewPDF, individualPDFs
import os
import pandas as pd

nameMailList = []
nameList = []

class FileUpload(QDialog):
    def __init__(self):
        super(FileUpload, self).__init__()
        self.imgDesignPath = None
        self.ssPath = None
        self.diplomasPath = None

        uic.loadUi("package/ui/FileUploadScreen.ui", self)
        
        # Evento de Boton
        self.btnChooseFileImg.clicked.connect(self.selectImg)
        self.btnChooseFileExcel.clicked.connect(self.selectExcel)
        self.btnGoBack.clicked.connect(self.goBack)
        self.btnPreviewTemplate.clicked.connect(self.previewTemplate)

    def setNavigation(self, screenController, previousScreen, nextScreen, mailScreen, finalScreen):
        self.screenController = screenController
        self.previousScreen = previousScreen
        self.nextScreen = nextScreen
        self.mailScreen = mailScreen
        self.finalScreen = finalScreen

    def setDiplomaFields(self, nombreTaller, namesAttributes, descriptionAttributes, dateAttributes, pdfSize, orientation):
        self.nombreTaller = nombreTaller
        self.namesAttributes = namesAttributes
        self.descriptionAttributes = descriptionAttributes
        self.dateAttributes = dateAttributes
        self.pdfSize = pdfSize
        self.orientation = orientation

    def selectImg(self):
        file = QFileDialog.getOpenFileName(filter="*.png *.jpg *.jpeg")
        path = file[0]
        file_extension = os.path.splitext(path)[1]

        if path == "":
            print("File not chosen.")
            return

        if file_extension not in [".png", ".jpg", ".jpeg"]:
            QMessageBox.warning(self, "Archivo no soportado", "Los archivos soportados son: .png, .jpg y .jpeg.")
            return

        self.imgDesignPath = path
            
        fileName = path.split('/')[-1]
        self.lbFileNameImg.setText(fileName)
        print(path)

    def selectExcel(self):
        file = QFileDialog.getOpenFileName(filter="*.xlsx *.xls")
        self.ssPath = file[0]
        file_extension = os.path.splitext(self.ssPath)[1]

        if self.ssPath == "":
            print("File not chosen.")
            return

        if file_extension not in [".xlsx", ".xls"]:
            QMessageBox.warning(self, "Archivo no soportado.", "Los archivos soportados son: .xlsx y .xls.")
            return

        fileName = self.ssPath.split('/')[-1]
        self.lbFileNameExcel.setText(fileName)

        if file_extension == ".csv":
            self.df = pd.read_csv(self.ssPath)
        else:
            self.df = pd.read_excel(self.ssPath)
            mails = pd.read_excel(self.ssPath, usecols='B')

        print(self.ssPath)
        print(self.df)

        mailList = self.df.values.tolist()
        for item in mailList:
            nameMailList.append(item)

        for item in nameMailList:
            nameList.append(item[0])

    def goBack(self):
        self.screenController.setCurrentWidget(self.previousScreen)
        
    def previewTemplate(self):
        global nameList, nameMailList

        if self.imgDesignPath == None or self.ssPath == None:
            QMessageBox.warning(self, "Archivo no seleccionado.", "Selecciona los archivos para continuar.")
            return
        
        previewPDF(self.df['Nombre'].to_list(), self.namesAttributes, self.descriptionAttributes, self.dateAttributes, self.imgDesignPath, self.pdfSize, self.orientation)
        self.diplomasPath = individualPDFs(self.nombreTaller, self.df['Nombre'].to_list(), self.namesAttributes, self.descriptionAttributes, self.dateAttributes, self.imgDesignPath, self.pdfSize, self.orientation)

        self.nextScreen.reloadPDF()
        self.finalScreen.setDiplomasPath(self.diplomasPath)
        self.mailScreen.setData(self.diplomasPath, nameList, nameMailList, self.nombreTaller)

        self.screenController.setCurrentWidget(self.nextScreen)
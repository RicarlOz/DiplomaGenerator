from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt5 import uic
from package.pdfGenerator import previewPDF, individualPDFs
from datetime import datetime
import os
import shutil
import pandas as pd

nameMailList = []
nameList = []
mailingList = []

class FileUploadEdit(QDialog):
    def __init__(self):
        super(FileUploadEdit, self).__init__()
        self.imgDesignPath = None
        self.ssPath = None
        self.diplomasPath = None

        uic.loadUi("package/ui/FileUploadEditScreen.ui", self)
        
        # Evento de Boton
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

    def setImageDesignPath(self, imgDesignPath):
        self.imgDesignPath = imgDesignPath

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

        for item in nameMailList:
            mailingList.append(item[1])

    def goBack(self):
        self.screenController.setCurrentWidget(self.previousScreen)
        
    def previewTemplate(self):
        global nameList, nameMailList, mailingList
        
        previewPDF(nameList, self.namesAttributes, self.descriptionAttributes, self.dateAttributes, self.imgDesignPath, self.pdfSize, self.orientation)
        self.diplomasPath = individualPDFs(self.nombreTaller, nameList, self.namesAttributes, self.descriptionAttributes, self.dateAttributes, self.imgDesignPath, self.pdfSize, self.orientation)

        self.nextScreen.reloadPDF()
        self.finalScreen.setDiplomasPath(self.diplomasPath)
        self.mailScreen.setData(self.diplomasPath, nameList, nameMailList, self.nombreTaller, mailingList)

        # Save template
        if not os.path.exists("package/templates/"):
            os.makedirs("package/templates/")
        
        if not os.path.exists("package/templateImages/"):
            os.makedirs("package/templateImages/")
        
        fileName = self.imgDesignPath.split('/')[-1]
        fileNameCache = fileName.split('.')[0] + datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + '.' + fileName.split('.')[1]
        shutil.copyfile(self.imgDesignPath, "package/templateImages/" + fileNameCache)

        data = {
            "Fecha" : datetime.today().strftime('%d-%m-%Y'),
            "NombreTaller" : self.nombreTaller,
            "ImageDesign": "package/templateImages/" + fileNameCache,
            "PDFSize": self.pdfSize,
            "PDFOrientation": self.orientation,
            "NombreFont": self.namesAttributes.font, 
            "NombreColor": f'{self.namesAttributes.color[0]}, {self.namesAttributes.color[1]}, {self.namesAttributes.color[2]}',
            "NombreSize": self.namesAttributes.size, 
            "DescripcionText": self.descriptionAttributes.text,
            "DescripcionFont": self.descriptionAttributes.font,
            "DescripcionColor": f'{self.descriptionAttributes.color[0]}, {self.descriptionAttributes.color[1]}, {self.descriptionAttributes.color[2]}',
            "DescripcionSize": self.descriptionAttributes.size,
            "DateText": self.dateAttributes.text,
            "DateFont": self.dateAttributes.font,
            "DateColor": f'{self.dateAttributes.color[0]}, {self.dateAttributes.color[1]}, {self.dateAttributes.color[2]}',
            "DateSize": self.dateAttributes.size
        }

        if os.path.exists("package/templates/templatesList.csv"):
            df_templates = pd.read_csv("package/templates/templatesList.csv")
            df_templates.loc[len(df_templates.index)] = data
        else:
            df_templates = pd.DataFrame(data, index=[0])

        df_templates.reset_index(inplace=True, drop=True)
        df_templates.to_csv("package/templates/templatesList.csv", index=False)        

        self.screenController.setCurrentWidget(self.nextScreen)
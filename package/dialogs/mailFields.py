from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QTextEdit
from PyQt5 import uic
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

testMails = [
    'csoftdiplomagendev@gmail.com', 
    'csoftdiplomagendev@gmail.com', 
    'csoftdiplomagendev@gmail.com', 
    'csoftdiplomagendev@gmail.com'
]

class MailFields(QDialog):
    def __init__(self):
        super(MailFields, self).__init__()

        # Cargar la config del archivo .ui en el objeto
        uic.loadUi("package/ui/MailFields.ui", self)

        # Definir Widgets
        self.btnBack = self.findChild(QPushButton, "btnBack")
        self.btnNext = self.findChild(QPushButton, "btnNext")
        self.tfAsunto = self.findChild(QLineEdit, "tfName")
        self.tfContenido = self.findChild(QTextEdit, "tfDescription")

        # Evento de botón
        self.btnBack.clicked.connect(self.goBack)
        self.btnNext.clicked.connect(self.submit)

    def setNavigation(self, screenController, previousScreen, nextScreen):
        self.screenController = screenController
        self.previousScreen = previousScreen
        self.nextScreen = nextScreen

    def setMail(self, correo):
        self.correo = correo

    def setPassword(self, password):
        self.password = password

    def setData(self, diplomasPath, nameList, nameMailList, nombreTaller, mailingList):
        self.diplomasPath = diplomasPath
        self.nameList = nameList
        self.mailingList = mailingList
        self.nameMailList = nameMailList
        self.nombreTaller = nombreTaller
        
    def goBack(self):
        self.screenController.setCurrentWidget(self.previousScreen)
    
    def submit(self):
        global testMails

        asuntoCorreo = self.tfAsunto.text()
        cuerpoCorreo = self.tfContenido.toPlainText()
        
        f = open(self.diplomasPath + "log.txt", "a+")
        f.write("Correo enviado a: \n")

        for name, mail in list(zip(self.nameList, self.mailingList)):
            message = MIMEMultipart()
            message['From'] = self.correo

            message.attach(MIMEText(cuerpoCorreo, 'html'))
            subj = asuntoCorreo + ' ' + name
            message['Subject'] = subj
            message['To'] = mail

            # Body and attachments for the mail
            pdfFilePath = self.diplomasPath + name + ' - ' + self.nombreTaller + '.pdf'
            attach_file_name = pdfFilePath
            attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
            payload = MIMEBase('application', 'octate-stream')
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload) #encode the attachment
            
            # Add payload header with filename
            payload.add_header('Content-Disposition', 'attachment', filename='Diploma.pdf')
            message.attach(payload)

            # Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
            session.starttls() #enable security
            
            session.login(self.correo, self.password) #login with mail_id and password
            text = message.as_string()
            session.sendmail(self.correo, mail, text)
            f.write(name + ' ' + mail + "\n")
            session.quit()

            del message, session
    
        f.close()

        self.nextScreen.openFolder()
        self.screenController.setCurrentWidget(self.nextScreen)

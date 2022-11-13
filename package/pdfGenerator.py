from fpdf import FPDF
import os
from datetime import datetime

libraryFonts = ['Arial', 'Courier', 'Helvetica', 'Symbol', 'Times', 'ZapfDingbats']
width = 170

class DataAttributes:
    def __init__(self, text = '', font = 'Arial', size = 16, color = (0, 0, 0)):
        self.text = text
        self.font = font
        self.size = size
        self.color = color

def previewPDF(names: list, namesAttributes: DataAttributes, descriptionAttributes: DataAttributes, dateAttributes: DataAttributes, imgDesign: str, pdfSize: str, orientation: str):

    #Creates the PDF document
    pdf = FPDF('L', 'mm', pdfSize)

    #Set margins
    pdf.set_margins(left=0, top=0, right=0)

    #Disable auto page break
    pdf.set_auto_page_break(False)

    #Add a page
    pdf.add_page()

    #Add font
    if not namesAttributes.font in libraryFonts:
        pdf.add_font(namesAttributes.font, "", 'package/fonts/' + namesAttributes.font + '.ttf', True)
    
    if not descriptionAttributes.font in libraryFonts:
        pdf.add_font(descriptionAttributes.font, "", 'package/fonts/' + descriptionAttributes.font + '.ttf', True)

    if not dateAttributes.font in libraryFonts:
        pdf.add_font(dateAttributes.font, "", 'package/fonts/' + dateAttributes.font + '.ttf', True)

    for name in names:
        
        #Add image
        if pdfSize == 'Letter':
            pdf.image(imgDesign, 0, 0, 279.4, 215.9)
        elif pdfSize == 'Legal':
            pdf.image(imgDesign, 0, 0, 356, 216)
        else: #A4
            pdf.image(imgDesign, 0, 0, 297, 210)

        ## Left
        if orientation == 'L':
            pdf.set_font(namesAttributes.font, '', namesAttributes.size)
            pdf.set_text_color(namesAttributes.color[0], namesAttributes.color[1], namesAttributes.color[2])
            pdf.set_xy(24, 82)
            pdf.cell(165, 10, txt=name, border=True, align='L')

            pdf.set_font(descriptionAttributes.font, '', descriptionAttributes.size)
            pdf.set_text_color(descriptionAttributes.color[0], descriptionAttributes.color[1], descriptionAttributes.color[2])
            pdf.set_xy(24, 100)
            pdf.multi_cell(165, 5, txt=descriptionAttributes.text, border=True, align='L')

            pdf.set_font(dateAttributes.font, '', dateAttributes.size)
            pdf.set_text_color(dateAttributes.color[0], dateAttributes.color[1], dateAttributes.color[2])
            pdf.set_xy(24, 150)
            pdf.cell(85, 15, txt=dateAttributes.text, border=True, align='L')
            
        ## Right
        elif orientation == 'R':
            pdf.set_font(namesAttributes.font, '', namesAttributes.size)
            pdf.set_text_color(namesAttributes.color[0], namesAttributes.color[1], namesAttributes.color[2])
            pdf.set_xy(92 - 25, 82)
            pdf.cell(165, 10, txt=name, border=True, align='R')

            pdf.set_font(descriptionAttributes.font, '', descriptionAttributes.size)
            pdf.set_text_color(descriptionAttributes.color[0], descriptionAttributes.color[1], descriptionAttributes.color[2])
            pdf.set_xy(92 - 25, 100)
            pdf.multi_cell(165, 5, txt=descriptionAttributes.text, border=True, align='R')

            pdf.set_font(dateAttributes.font, '', dateAttributes.size)
            pdf.set_text_color(dateAttributes.color[0], dateAttributes.color[1], dateAttributes.color[2])
            pdf.set_xy(172 - 25, 150)
            pdf.cell(85, 15, txt=dateAttributes.text, border=True, align='R')

        ## Center
        else:
            pdf.set_font(namesAttributes.font, '', namesAttributes.size)
            pdf.set_text_color(namesAttributes.color[0], namesAttributes.color[1], namesAttributes.color[2])
            pdf.set_xy((279.4 / 2 - width / 2) + 10, 120)
            pdf.cell(width, 10, txt=name, border=False, align='C')

            pdf.set_font(descriptionAttributes.font, '', descriptionAttributes.size)
            pdf.set_text_color(descriptionAttributes.color[0], descriptionAttributes.color[1], descriptionAttributes.color[2])
            pdf.set_xy((279.4 / 2 - width / 2) + 10, 135)
            pdf.multi_cell(width, 5, txt=descriptionAttributes.text, border=False, align='C')

            pdf.set_font(dateAttributes.font, '', dateAttributes.size)
            pdf.set_text_color(dateAttributes.color[0], dateAttributes.color[1], dateAttributes.color[2])
            pdf.set_xy(180, 195)
            pdf.cell(85, 15, txt=dateAttributes.text, border=False, align='C')
            
        if name != names[-1]:
            pdf.add_page()

    pdf.output("diplomas.pdf")
    del pdf

def individualPDFs(eventName: str, names: list, namesAttributes: DataAttributes, descriptionAttributes: DataAttributes, dateAttributes: DataAttributes, imgDesign: str, pdfSize: str, orientation: str) -> str:
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")

    if eventName in ['', None]:
        diplomasPath = os.path.join(os.path.abspath(os.getcwd()), "Diplomas\\Evento " + dt_string + '\\')
    else:
        diplomasPath = os.path.join(os.path.abspath(os.getcwd()), "Diplomas\\" + eventName + '\\')
    
    if not os.path.exists(diplomasPath):
        os.makedirs(diplomasPath)                

    for name in names:
        #Creates the PDF document
        pdf = FPDF('L', 'mm', pdfSize)
        # pdf = FPDF('L', 'mm', 'Letter')

        #Set margins
        pdf.set_margins(left=0, top=0, right=0)

        #Disable auto page break
        pdf.set_auto_page_break(False)

        #Add a page
        pdf.add_page()

        #Add font
        if not namesAttributes.font in libraryFonts:
            pdf.add_font(namesAttributes.font, "", 'package/fonts/' + namesAttributes.font + '.ttf', True)
        
        if not descriptionAttributes.font in libraryFonts:
            pdf.add_font(descriptionAttributes.font, "", 'package/fonts/' + descriptionAttributes.font + '.ttf', True)

        if not dateAttributes.font in libraryFonts:
            pdf.add_font(dateAttributes.font, "", 'package/fonts/' + dateAttributes.font + '.ttf', True)

        #Add image
        if pdfSize == 'Letter':
            pdf.image(imgDesign, 0, 0, 279.4, 215.9)
        elif pdfSize == 'Legal':
            pdf.image(imgDesign, 0, 0, 356, 216)
        else: #A4
            pdf.image(imgDesign, 0, 0, 297, 210)

        ## Left
        if orientation == 'L':
            pdf.set_font(namesAttributes.font, '', namesAttributes.size)
            pdf.set_text_color(namesAttributes.color[0], namesAttributes.color[1], namesAttributes.color[2])
            pdf.set_xy(24, 82)
            pdf.cell(165, 10, txt=name, border=True, align='L')

            pdf.set_font(descriptionAttributes.font, '', descriptionAttributes.size)
            pdf.set_text_color(descriptionAttributes.color[0], descriptionAttributes.color[1], descriptionAttributes.color[2])
            pdf.set_xy(24, 100)
            pdf.multi_cell(165, 5, txt=descriptionAttributes.text, border=True, align='L')

            pdf.set_font(dateAttributes.font, '', dateAttributes.size)
            pdf.set_text_color(descriptionAttributes.color[0], descriptionAttributes.color[1], descriptionAttributes.color[2])
            pdf.set_xy(24, 150)
            pdf.cell(85, 15, txt=dateAttributes.text, border=True, align='L')

            
            
        ## Right
        elif orientation == 'R':
            pdf.set_font(namesAttributes.font, '', namesAttributes.size)
            pdf.set_text_color(namesAttributes.color[0], namesAttributes.color[1], namesAttributes.color[2])
            pdf.set_xy(92 - 25, 82)
            pdf.cell(165, 10, txt=name, border=True, align='R')

            pdf.set_font(descriptionAttributes.font, '', descriptionAttributes.size)
            pdf.set_text_color(descriptionAttributes.color[0], descriptionAttributes.color[1], descriptionAttributes.color[2])
            pdf.set_xy(92 - 25, 100)
            pdf.multi_cell(165, 5, txt=descriptionAttributes.text, border=True, align='R')

            pdf.set_font(dateAttributes.font, '', dateAttributes.size)
            pdf.set_text_color(dateAttributes.color[0], dateAttributes.color[1], dateAttributes.color[2])
            pdf.set_xy(172 - 25, 150)
            pdf.cell(85, 15, txt=dateAttributes.text, border=True, align='R')

            

        ## Center
        else:
            pdf.set_font(namesAttributes.font, '', namesAttributes.size)
            pdf.set_text_color(namesAttributes.color[0], namesAttributes.color[1], namesAttributes.color[2])
            pdf.set_xy((279.4 / 2 - width / 2) + 10, 120)
            pdf.cell(width, 10, txt=name, border=False, align='C')

            pdf.set_font(descriptionAttributes.font, '', descriptionAttributes.size)
            pdf.set_text_color(descriptionAttributes.color[0], descriptionAttributes.color[1], descriptionAttributes.color[2])
            pdf.set_xy((279.4 / 2 - width / 2) + 10, 135)
            pdf.multi_cell(width, 5, txt=descriptionAttributes.text, border=False, align='C')

            pdf.set_font(dateAttributes.font, '', dateAttributes.size)
            pdf.set_text_color(dateAttributes.color[0], dateAttributes.color[1], dateAttributes.color[2])
            pdf.set_xy(180, 195)
            pdf.cell(85, 15, txt=dateAttributes.text, border=False, align='C')

        pdf.output(diplomasPath + name + ' - ' + eventName + '.pdf')
        
    return diplomasPath
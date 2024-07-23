from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors


filename = 'Receipt.pdf'
documentTitle = 'Receipt'
custom_size = (400, 600)

pdf = canvas.Canvas(filename, pagesize=custom_size)
pdf.setTitle(documentTitle)
pdfmetrics.registerFont(TTFont('abc', 'SakBunderan.ttf'))

# Border set up.
pdf.setStrokeColor(colors.black)
pdf.setFillColor(colors.white)
pdf.rect(20, 20, 360, 560)

# Line has been drawn.
pdf.line(20, 480, 380, 480)
pdf.line(20, 450, 380, 450)
pdf.line(20, 330, 380, 330)
pdf.line(20, 300, 380, 300)
pdf.line(20, 100, 380, 100)

# Cross Lines.
pdf.line(60, 100, 60, 330)
pdf.line(300, 100, 300, 330)

image1 = 'Logo.jpeg'


image2 = 'Sign.jpeg'


pdf.drawInlineImage(image1, 25, 495, 60, 80)
pdf.drawInlineImage(image2, 280, 30, 30, 30)

address_line1 = "123 Learning Lane"
address_line2 = "Knowledge City, IN 45678"
address_line3 = "Phone: (555) 123-4567"

pdf.setFillColorRGB(0, 0, 0)
pdf.setFont('Helvetica-Bold', 14)
pdf.drawCentredString(200, 555, 'KRISHNA COACHING CENTER')
pdf.setFont('Helvetica', 12)
pdf.drawString(95, 535, address_line1)
pdf.drawString(95, 515, address_line2)
pdf.drawString(95, 495, address_line3)

# Basic Student Details.
Name = 'Mahesh Nayak'
Id = '4MT21CS077'
Branch = 'Computer Science And Enginnering'
Date = '21/06/2023'

pdf.setFillColorRGB(0, 0, 0)
pdf.setFont('Courier-Bold', 14)

pdf.drawString(21, 430, 'NAME: '+Name)
pdf.drawString(21, 400, 'ID: '+Id)
pdf.drawString(21, 370, 'BRANCH: '+Branch)
pdf.drawString(21, 340, 'DATE: '+Date)


pdf.setFillColorRGB(0, 0, 0)
pdf.setFont('Courier-Bold', 16)
pdf.drawCentredString(180, 465, 'RECEIPT')

pdf.setFont('Courier-Bold', 14)
pdf.drawCentredString(40, 315, 'Sl')
pdf.drawCentredString(180, 315, 'Particulars')
pdf.drawCentredString(340, 315, 'Amount')


particulars = 'Examination Fees'
amount = '1780'

pdf.setFont('Courier-Bold', 12)
pdf.drawCentredString(40, 280, '1')
pdf.drawString(65, 280, particulars)
pdf.drawCentredString(340, 280, amount)

pdf.setFont('Courier-Bold', 14)
pdf.drawCentredString(270, 120, 'TOTAL')

total = '1780'
pdf.setFont('Courier-Bold', 12)
pdf.drawCentredString(340, 120, total)

InWords = 'One Thousand Seven Hundred eighty only'
pdf.setFont('Courier-Bold', 12)
pdf.drawString(20, 80, 'In Words: ')
pdf.drawString(85, 80, InWords)

pdf.drawString(225, 22, 'Authorized Signature')


pdf.save()
import PyPDF2

#Read PDF
my_file = open('paper.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(my_file)

#Print number of pages
print(pdf_reader.numPages)

#PDF pages to images
from pdf2image import convert_from_path
images = convert_from_path("paper1.pdf", 500,poppler_path=r'C:/Users/hp/Desktop/Fleurissant_Résumé_Project/poppler-0.68.0/bin')
for i, image in enumerate(images):
    fname = 'image'+str(i)+'.png'
    image.save(fname, "PNG")




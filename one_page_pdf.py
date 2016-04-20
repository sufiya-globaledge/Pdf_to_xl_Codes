import PyPDF2

#Below lines of code to converts one page of main pdf into other pdf file
pdf1File =open('ALL.pdf', 'rb')
pdf1Reader = PyPDF2.PdfFileReader(pdf1File)

pdfWriter = PyPDF2.PdfFileWriter()

pageObj = pdf1Reader.getPage(0)
pdfWriter.addPage(pageObj)

pdfOutputFile = open('one_page_pdf.pdf', 'wb')
pdfWriter.write(pdfOutputFile)

pdfOutputFile.close()
pdf1File.close()

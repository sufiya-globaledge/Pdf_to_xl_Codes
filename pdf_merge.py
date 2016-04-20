from PyPDF2 import PdfFileMerger, PdfFileReader

merger = PdfFileMerger()
for filename in ['ALL.pdf','AML.pdf']:
    merger.append(PdfFileReader(file(filename, 'rb')))

merger.write("document-output.pdf")


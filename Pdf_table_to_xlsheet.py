#Below code for fetching table from pdf and importing into xlsheet in proper formatt

import PyPDF2
import codecs
import re
import xlrd
import xlwt
import urllib2
import xml.etree.ElementTree as ET


#Open given pdf in read mode
pdfFileObj = open('document-output.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

#Print number of pages in pdf
Num_pages = pdfReader.numPages
 

#extracts one page from main pdf and converts into pdf formatt, to fetch elements of 1st column of each table.
#To create 'one_page_pdf' file use 'one_page_pdf.py', script.
pdfdata = open('one_page_pdf.pdf', 'rb').read()

#Create xlsheet to save results
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")
style = xlwt.XFStyle()

# Set font for text
font = xlwt.Font()
font.bold = True
style.font = font

try :
  #Converts pdfdata provided to 'xml' formatt
  request = urllib2.Request('http://pdfx.cs.man.ac.uk', pdfdata, headers={'Content-Type' : 'application/pdf'})
  response = urllib2.urlopen(request).read()
except:
  print "Raise exception :Error occure while converting pdf to xml "


# Parse the response to get tree structure to fetch elements from xml
tree = ET.fromstring(response)

try:
#Below line of code is to searchand save elements of 1st column of each table
#Stored all element of 1st column in list1
  b=[]
  for tbox in tree.findall('.//outsider[@type="sidenote"]'):
    bb = tbox.text
    dd = bb.split(":")
    b.append(dd)


  for tbox in tree.findall('.//abstract[@class="DoCO:Abstract"]'):
      f = tbox.text
      y =f.split(":")
      del y[-1]

  y.extend([b[0][0],b[1][0],b[1][1],b[1][2],b[2][0]])
  list1 = [ s + ":"  for s in y]
  list1 = [x.strip(' ') for x in list1]
  list1.append("!")

except:
  print "Raise exception: error occured during searching elemnts"


#Below lines of code is for fetching elemts from 2nd column of each table.
#Stores all elements into xlsheet 

row = 1
# Adjusted  width * length of column
col_width = 256 * 40 
try :
 for i in range(Num_pages):
   #created empty list to store elemnts of 2nd column of each table
   y = []
   #Created page object to perform operation on pdf
   pageObj = pdfReader.getPage(i)
   #Extracted text from each page of original pdf into 'output.txt' file
   data =pageObj.extractText()
   data = " ".join(data.replace(u"\xa0", " ").strip().split())
   with codecs.open("Output.txt", "w",encoding='utf8')as text_file:
       text_file.write(data)
   
   f = open('Output.txt','r')
   data1 = f.read()
   
   #below line of code generate pattern for searching 2nd column elements into text file   
   for first, second in zip(list1, list1[1:]):
      #print first, second
      z = first + "(.*?)" + second

      x = re.findall(z,data1,re.DOTALL)

      y.append(x)

   
   #Write all elements into xlsheet
   sheet1.col(row -1).width = col_width
   for index, value in enumerate(list1[:-1]):
	sheet1.write(row-1, index, value.split(':')[0], style=style)

   sheet1.col(row).width = col_width
   for index, value in enumerate(y):
        sheet1.write(row, index, value)

   row = row + 2

 book.save('pdf_table_to_xlsheet.xls')

except:
  print "Raise exception: Error occur while updating to xlsheet or fetching elements from pdf"


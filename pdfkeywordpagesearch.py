from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import PDFPageAggregator
import pdfminer
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure
from PyPDF2 import PdfFileWriter, PdfFileReader

path = '/opt/mycroft/skills/skill-pdf/'




input = ['windows' ]

# thefile = open('test.txt', 'w')
#
#
# for item in input:
#   thefile.write("%s\n" % item)
#
# thefile.close()


text_file = open(path +'test.txt', 'r')

Keywords = text_file.read().split()

text_file.close()

print(Keywords)



def createPDFDoc(fpath):
    fp = open(fpath, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser, password='')
    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise "Not extractable"
    else:
        return document


def createDeviceInterpreter():
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    return device, interpreter


def parse_obj(objs):
    counter = 0
    for obj in objs:
        if isinstance(obj, pdfminer.layout.LTTextBox):
            for o in obj._objs:

                if isinstance(o,pdfminer.layout.LTTextLine) and \
                        isinstance(o._objs[0], pdfminer.layout.LTChar):


                # if isinstance(o, pdfminer.layout.LTTextLine) and \
                #         isinstance(o._objs[0], pdfminer.layout.LTChar) and \
                #                 o._objs[0].fontname == 'Times-Bold' and \
                #                 o._objs[0].adv > 0.666:

                    LineOfText= o.get_text()
                    #print(LineOfText)
                    lowercaseLineOfText = LineOfText.lower()
                    words = lowercaseLineOfText.split()



                    # print "fontname %s" % o._objs[0].fontname
                    # print(o._objs[0].adv)
                    # print(words)

                    for speechword in Keywords:
                        if speechword in words:
                            #print('Found Here', str(counter))
                            counter = counter + 1
                            #return counter

        # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj(obj._objs)
        else:
            pass

    return counter



# Open a PDF file.
fp = open('/home/david/Downloads/Ben Clark - Red Team Field Manual.pdf', 'rb')



# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)

# Create a PDF document object that stores the document structure.
# Password for initialization as 2nd parameter
document = PDFDocument(parser)

# Check if the document allows text extraction. If not, abort.
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed

# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()

# Create a PDF device object.
device = PDFDevice(rsrcmgr)

# BEGIN LAYOUT ANALYSIS
# Set parameters for analysis.
laparams = LAParams()

# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)

# Create a PDF interpreter object.
interpreter = PDFPageInterpreter(rsrcmgr, device)


file1 = PdfFileReader(file('/home/david/Downloads/Ben Clark - Red Team Field Manual.pdf', "rb") , strict = False)


output = PdfFileWriter()


count = 1

for page in PDFPage.create_pages(document):

    if count >= 1:
        print("###################################################################", count ,"########################################################")
        #print(page)
        # read the page into a layout object
        interpreter.process_page(page)
        layout = device.get_result()
        #interpreter2.process_page(page)
        #parse_layout(layout)

        # extract text from this object
        parse_obj(layout._objs)
        print(type(parse_obj(layout._objs)))
        if parse_obj(layout._objs) > 0:
            print(parse_obj(layout._objs))
            output.addPage(file1.getPage(count))
    count = count + 1

outputStream = file(path + 'document-output.pdf', "wb")
output.write(outputStream)
outputStream.close()



import webbrowser
webbrowser.open(r'/opt/mycroft/skills/skill-pdf/document-output.pdf')


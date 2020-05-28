'''Makes a PDF of a user's channel - 1 video thumbail PER page
and description - ie 100 videos, 100 page PDF!'''
import codecs
import os
import sys
from fpdf import FPDF
from tqdm import tqdm
import json
import unicodedata
import time

class PdfMaker(object):

                def __init__(self):
                    self.tx = "Blaaaaaaaaaah"
                    self.insertimage = ""
                    self.pdfname = "output.pdf"
                    self.spath = "youtube_downloads"
                    self.djpg = {}
                    self.jsonf = {}
                    self.fd = ""
                    self.mdic = {}


                def list_dir(self): 
                    """ List directories inside youtube downloads for user to chosoe from"""
                    x = [x for x in os.listdir(self.spath) if os.path.isdir(os.path.join(self.spath, x))]
                    if x != [] :
                        print (f"choose one of these : {x}")


                def ask_user(self):
                    self.res = input("Enter name of folder to use, and press Enter: ")
                    self.fd = (self.spath +"/" + self.res)
                    print (f"There are n files in {self.fd} this may take a while")
                    #add progress bar
                    
                    print(self.fd)
                    for file in os.listdir(self.fd):
                            if file.endswith(".jpg"):
                                    jpgpdf = (os.path.join(self.fd, file))
                                    self.djpg[file] = jpgpdf                               


                def make_pdf(self):

                    
                 
                    
                    with open (self.fd + "/" + "_desc.json", "r") as js:
                        self.mdic = json.load(js)

                    pdf = FPDF()

                    for k,v in self.mdic.items():

                        vtit = (v[1][1])
                        vid= (v[0][1])
                        vdes = (v[2][1])
                        print(vtit)
                        pdf.add_page()
                        pdf.image('logo.png', 10, 8, 33,0,'', 'http://www.redandgreen.co.uk')
                        image_path = (self.fd +"/" + vid + ".jpg")
                        pdf.image(image_path,10, 30, 190,0,'', "http://www.youtube.com/watch?v="+ vid)
                        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
                        pdf.set_font('DejaVu', '', 14)
             
                        pdf.cell(180, 15, txt="http://www.youtube.com/watch?v="+ vid, ln=1, align="L")
                        pdf.cell(30, txt="{}".format(vtit), ln=1, align="L")
                        pdf.ln(165) # comment out if error
                        pdf.multi_cell(w=0, h=4, txt=vdes) # comment out if error

                    for i in tqdm(range(20)):
                        pdf.output(self.pdfname, 'F')
                        time.sleep(0.5)


                    print("All done, please check root folder for output.pdf")

if __name__ == '__main__':

                mypdf = PdfMaker()
                mypdf.list_dir()
                mypdf.ask_user()
                mypdf.make_pdf()
      


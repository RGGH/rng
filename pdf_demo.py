import os
import sys
from fpdf import FPDF
from tqdm import tqdm
import json

class PdfMaker(object):

                def __init__(self):
                    self.tx = "Blaaaaaaaaaah"
                    self.insertimage = ""
                    self.pdfname = "OP.pdf"
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
                        #print (self.mdic)

                        pdf = FPDF()
                        
                        for k,v in self.mdic.items():
                            print(f"Video Title = ",v[1][1])
                            print(f"Video ID = ",v[0][1])
                            print(f"Video Description = ",v[2][1])
                            vtit = (v[1][1])
                            vid= (v[0][1])
                            vdes = (v[2][1])
                            
                            pdf.add_page()
                            pdf.image('logo.png', 10, 8, 33)
                            image_path = self.fd +"/" + vid + ".jpg"
                            pdf.image(image_path,x=10, y=30, w=190)
                            pdf.set_font("Arial", size=12)
                            pdf.cell(190, 10, txt="{}".format(vtit), ln=1, align="C")
                            pdf.ln(185)
                            #pdf.cell(200, 10, txt="{}".format(image_path), ln=1)
                            #pdf.cell(180, 10, txt="{}".format(vdes), ln=4, align="L")
                            pdf.multi_cell(w=0, h=5, txt=vdes)
                            #response.headers['Content-Type'] = 'application/pdf'
                        pdf.output(self.pdfname)

                        print("All done, please check root folder for OP.pdf")

if __name__ == '__main__':

                mypdf = PdfMaker()
                mypdf.list_dir()
                mypdf.ask_user()
                mypdf.make_pdf()
      


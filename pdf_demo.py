import os
import sys
from fpdf import FPDF
from tqdm import tqdm

class PdfMake(object):

	def __init__(self):
		self.tx = "Blaaaaaaaaaah"
		self.insertimage = ""
		self.pdfname = "OP.pdf"
		self.spath = "youtube_downloads"
		self.djpg = {}

	def list_dir(self): 
        	""" List directories inside youtube downloads for user to chosoe from"""
        	x = [x for x in os.listdir(self.spath) if os.path.isdir(os.path.join(self.spath, x))]
        	if x != [] :
            		print (f"choose one of these : {x}")


	def ask_user(self):
		self.res = input("Enter name of folder to use, and press Enter: ")
		fd = (self.spath +"/" + self.res)
		print (f"There are n files in {fd} this may take a while")
		#add progress bar
		fd = (self.spath +"/" + self.res)
		print(fd)
		for file in os.listdir(fd):
			if file.endswith(".jpg"):
				jpgpdf = (os.path.join(fd, file))
				self.djpg[file] = jpgpdf
				print(self.djpg)

	def make_pdf(self):
		pdf = FPDF()
		for k,v in self.djpg.items():
			image_path = v
			pdf.add_page()
			pdf.image(image_path,x=55, y=30, w=100)
			pdf.set_font("Arial", size=12)
			pdf.cell(190, 10, txt="Dr Pi Pdf From Python", ln=1, align="C")
			pdf.ln(185)
			pdf.cell(200, 10, txt="{}".format(image_path), ln=1)
			pdf.cell(200, 10, txt="{}".format(image_path), ln=1, align="C")
		pdf.output(self.pdfname)

if __name__ == '__main__':

	pdf = PdfMake()
	pdf.list_dir()
	pdf.ask_user()
	pdf.make_pdf()


from fpdf import FPDF
from PIL import Image
import os

def createpdf(foldertoget):
    patha = os.path.expanduser('~/Desktop/CIAN')

    if os.path.exists(patha+'/pdf/'+"bot.pdf"):
        os.remove(patha+'/pdf/'+"bot.pdf")
    pdf = FPDF(orientation='L', unit='mm', format='A4')

    c = 1
    hi = []
    wi = []
    for i in range(0, 100):
        try:
            p = Image.open(patha+"/files/"+foldertoget+"/" + str(i) + ".png")
            w, h = p.size
            if w > h:
                wi.append(patha+"/files/"+foldertoget+"/" + str(i) + ".png")
            else:
                hi.append(patha+"/files/"+foldertoget+"/" + str(i) + ".png")
        except Exception:
            a = 0

    if len(wi) != 0:
        pdf.add_page()
        for N in range(0,4+len(wi)//4):
            if N>len(wi):break
            try:
                pdf.set_xy(6, 1)
                pdf.image(wi[N*4], w=130, h=90)
                pdf.set_xy(140, 1)
                pdf.image(wi[N*4+1], w=130, h=90)
                pdf.set_xy(6, 94)
                pdf.image(wi[N*4+2], w=130, h=90)
                pdf.set_xy(140, 94)
                pdf.image(wi[N*4+3], w=130, h=90)
                if len(wi)>N*4+4:
                    pdf.add_page()
            except Exception:
                break

    if len(hi) !=0:pdf.add_page()

    for N in range(0,2+len(hi)//2):
        if N > len(hi): break
        try:
            pdf.set_xy(6, 2)
            pdf.image(hi[N*2], w=135, h=185)
            pdf.set_xy(152, 2)
            pdf.image(hi[N*2+1], w=135, h=185)
            if len(hi)!=N*2+2:
                pdf.add_page()
        except Exception:
            break
    if len(hi)==0 or len(wi)==0: c = c + 1
    pdf.output(patha+'/pdf/'+"bot.pdf")
    return c

##DejaVuSansCondensed.ttf
#DejaVuSansCondensed.ttf



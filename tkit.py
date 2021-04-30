import pdfkit
from shutil import copyfile
import os

def newpdf(adr,desc,t1,v1,t2,v2,t3,v3,t4,v4,t5,v5,met,prc):
    path_to = os.path.expanduser('~/Desktop/CIAN/')
    if os.path.exists(path_to+"pdf/top.pdf"):
        os.remove(path_to+"pdf/top.pdf")

    copyfile(path_to+'a.html', path_to+'t.html')
    copyfile(path_to+'files/map/map.png', path_to+'files/map/m.png')
    fpath = path_to+'t.html'

    desc.replace('\n','<br>')

    with open(fpath,encoding='UTF-8') as f:
        s = f.read()
    s = s.replace("#ADR#", adr)
    s = s.replace("#desc#", desc)
    for each in met.keys():
        s = s.replace("#metro#", "<li>"+str(met[each])+str(each)+"</li>#metro#")

    s = s.replace("#prc#", prc)

    s = s.replace("#metro#", "")
    s = s.replace("#desc#", desc)

    if t1.strip() != '':
        s = s.replace("#t#", "<tr><td>"+t1+"</td><td><strong>"+v1+"</strong></td></tr>#t#")

    if t2.strip() != '':
        s = s.replace("#t#", "<tr><td>"+t2+"</td><td><strong>"+v2+"</strong></td></tr>#t#")

    if t3.strip() != '':
        s = s.replace("#t#", "<tr><td>"+t3+"</td><td><strong>"+v3+"</strong></td></tr>#t#")

    if t4.strip() != '':
        s = s.replace("#t#", "<tr><td>"+t4+"</td><td><strong>"+v4+"</strong></td></tr>#t#")

    if t5.strip() != '':
        s = s.replace("#t#", "<tr><td>"+t5+"</td><td><strong>"+v5+"</strong></td></tr>#t#")

    s = s.replace("#t#",'')

    with open(fpath, "w",encoding='UTF-8') as f:
        f.write(s)

    options = {
        "enable-local-file-access": None
    }
    #config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    #pdfkit.from_file('t.html', 'MyPDF.pdf', configuration=config,options=options)
    pdfkit.from_file(path_to+'t.html', path_to+"pdf/top.pdf", options=options)

    os.remove(path_to+'t.html')
    os.remove(path_to+'files/map/m.png')
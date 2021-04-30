#!/usr/bin/python3
import requests
from tkinter import *
from bs4 import BeautifulSoup
from func import *
from photos import *
from form_pdf import *
from tkit import newpdf
from PyPDF2 import PdfFileMerger
import threading
from fp.fp import FreeProxy
import subprocess
import os
import tkinter.scrolledtext as st
import re
import clipboard

WDT = 20
DESC = ''
hYEAR = ''
hSQ = ''
hSQALL = ''
hFLOOR = ''
hDATE = ''
ADDRESS = ''
PHOTONUM = 0
proxxxy = None
met = {}

def _onKeyRelease(event):
    ctrl  = (event.state & 0x4) != 0
    if event.keycode==88 and  ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")
    if event.keycode==86 and  ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")
    if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")
def validate(possible_new_value):
    if re.match(r'^[0-9a-fA-F]*$', possible_new_value):
        return True
    return False
def newinf(status):
    infol.config(text=status)
def textc_upd(one, two):
    res = ''
    for each in one:
        res = res + each + ';\n'

    for each in two:
        res = res + each + ';\n'
    textc.insert(1.0, res)
def clean_CIAN():
    ent.delete(0, END)

def clipboard_CIAN():
    ent.insert(1, clipboard.paste())
def parse_CIANthre():
    veryB.configure(state=DISABLED)
    newinf("Скачиваю изображения")
    threading.Thread(target=parse_CIAN).start()

def upd_shit(shit):
    first = shit[:len(shit)//2]
    second = shit[len(shit)//2:]

    try:
        ent1.insert(1,first[0])
        ent3.insert(1, first[1])
        ent5.insert(1, first[2])
        ent7.insert(1, first[3])
        ent9.insert(1, first[4])
    except Exception:
        pass
    try:
        ent2.insert(1,second[0])
        ent4.insert(1,second[1])
        ent6.insert(1,second[2])
        ent8.insert(1,second[3])
        ent10.insert(1,second[4])
    except Exception:
        pass

def mrproper():
    text.delete(1.0, END)
    textc.delete(1.0, END)
    hhent.delete(0, END)
    ent1.delete(0, END)
    ent2.delete(0, END)
    ent3.delete(0, END)
    ent4.delete(0, END)
    ent5.delete(0, END)
    ent6.delete(0, END)
    ent7.delete(0, END)
    ent8.delete(0, END)
    ent9.delete(0, END)
    ent10.delete(0, END)
    ec.delete(0, END)

def crpdf():
    global path_to
    global met
    bg = {}
    a = (' '+textc.get(1.0, END)).split(';')
    a.pop()
    co = 0
    for each in met.keys():
        bg[a[co]] = met[each]
        co = co+1
    try:
        for each in a[co:]:
            bg[each] = ''
    except Exception:
        co = co+1

    newpdf(hhent.get(),((text.get(1.0, END)).replace("\n","<br>")),ent1.get(),ent2.get(),
           ent3.get(),ent4.get(),ent5.get(),ent6.get(),
           ent7.get(),ent8.get(),ent9.get(),ent10.get(),bg,ec.get())
    createpdf("processed")
    merger = PdfFileMerger()
    try:
        pdfname = str(hhent.get().strip().split(',')[-2]) + str(hhent.get().strip().split(',')[-1])
        pdfname = ''.join(c for c in pdfname if c.isalpha() or c.isdecimal())
    except Exception:
        pdfname = "result"
    merger.append(path_to + '/pdf/top.pdf')
    merger.append(path_to + '/pdf/bot.pdf')
    #проверка на уникальность 
    if os.path.exists(path_to + '/pdf/'+pdfname+'.pdf'):
        index = pdfname.find('((')
        if index == -1:
            pdfname = pdfname + '((' + str(1) + '))'
        else:
            cpnum = int(pdfname[index+2:-2])
            pdfname = pdfname[:index] + '((' + str(cpnum+1) + '))'  
    merger.write(path_to + '/pdf/'+ pdfname  + '.pdf')
    merger.close()
    newinf("PDF создан!")

def crpdfmask():
    global path_to
    global met
    bg = {}
    a = (' '+textc.get(1.0, END)).split(';')
    a.pop()
    co = 0
    for each in met.keys():
        bg[a[co]] = met[each]
        co = co+1
    try:
        for each in a[co:]:
            bg[each] = ''
    except Exception:
        co = co+1

    newpdf(hhent.get(),((text.get(1.0, END)).replace("\n","<br>")),ent1.get(),ent2.get(),
           ent3.get(),ent4.get(),ent5.get(),ent6.get(),
           ent7.get(),ent8.get(),ent9.get(),ent10.get(),bg,ec.get())
    createpdf("noCIAN")
    merger = PdfFileMerger()
    try:
        pdfname = str(hhent.get().strip().split(',')[-2]) + str(hhent.get().strip().split(',')[-1])
        pdfname = ''.join(c for c in pdfname if c.isalpha() or c.isdecimal())
    except Exception:
        pdfname = "result"
    merger.append(path_to + '/pdf/top.pdf')
    merger.append(path_to + '/pdf/bot.pdf')
    merger.write(path_to + '/pdf/'+pdfname+'.pdf')
    merger.close()
    newinf("PDF создан!")


def insert_text():
    s = ""
    text.insert(1.0, s)
def get_text():
    s = text.get(1.0, END)
    #label['text'] = s
def delete_text():
    text.delete(1.0, END)

def proxnew():
    global proxxxy
    newinf("Ищу рабочий прокси")
    proxxxy = FreeProxy(rand=True).get()
    newinf("Прокси обновлен")
    pr_ent.insert(1, proxxxy)
def reqget(href):
    global proxxxy
    try:
        if proxxxy is None or proxxxy == '':
            r = requests.get(href)
        else:
            proxyDict = {
                "http": proxxxy,
                "ftp": proxxxy
            }
            r = requests.get(href, proxies=proxyDict)
        res = []
        res.append(r.content)
        res.append(r.text)
        return res
    except Exception:
        return None
def parse_CIAN():
    global DESC, ADDRESS, PHOTONUM, met,proxxxy
    proxxxy = str(pr_ent.get()).strip()
    mrproper()

    req = reqget(ent.get())
    if req is not None:
        html = req[0]
        soup = BeautifulSoup(html, 'html.parser')
        try:
            DESC = find_description(soup)
            ADDRESS = find_head(soup)
            hhent.insert(1, ADDRESS)
            text.insert(1.0, DESC)
            upd_shit((find_shit(soup)))
            ec.insert(1, find_price(soup))
            met = find_metro(soup)
            textc_upd(met.keys(), find_high(soup))
            photos_list = getphot(req[1])
            delall()
            processuka(photos_list)
            downloadphotos(photos_list)
            veryB.configure(state=NORMAL)
            newinf("Скачивание завершено")
        except Exception:
            print(str(Exception))
            newinf("ЦИАН включил блок, обновите прокси")
    else:
        newinf("Не удалось выполнить запрос, обновите прокси и прверьте соединение")
    veryB.configure(state=NORMAL)
def downloadphotos(rows):
    global path_to
    counter = 0
    eblan = []
    os.mkdir(path_to + '/files/downloaded')
    os.mkdir(path_to + '/files/processed')
    os.mkdir(path_to + '/files/noCIAN')
    for i in rows:

        file_name = path_to + '/files/downloaded/' + str(counter) + '.jpeg'
        newinf("Скачиваю " + file_name)

        req = reqget(i)
        if req is not None:
            file = open(file_name, "wb")
            file.write(req[0])
            file.close()

            threading.Thread(target=jopa, args=(counter, file_name,)).start()

            try:
                newinf('Обрабатываю ' + str(counter) + '.jpeg')
                photo = Image.open(path_to + '/files/downloaded/' + str(counter) + '.jpeg')
                watermark = Image.open(path_to + '/logo.png')
                wi, he = photo.size
                watermark.thumbnail(photo.size)
                w2, h2 = watermark.size
                photo.paste(watermark, (0, (he - h2) // 2), watermark)
                photo.save(path_to + '/files/processed/' + str(counter) + '.png', "PNG")
                eblan.append((wi, he))
            except Exception:
                pass
            counter += 1
    # newinf('...')

def goIMG():
    subprocess.Popen(['open','R','~/PycharmProjects'])
def goPDF():
    print(open, '~/PycharmProjects')


path_to = os.path.expanduser('~/Desktop/CIAN')
try:
    os.mkdir(path_to + '/files')
    os.mkdir(path_to + '/pdf')
except Exception:
    pass

root = Tk()
root.title("CIAN PDF")

f_ULTRA = Frame()
f_ULTRA.pack(padx=10)

f_top_pro = LabelFrame(f_ULTRA,text="Прокси",padx=10,pady=10)
f_top_pro.pack(side=LEFT)

Button(f_top_pro, text="*",
       command=proxnew).pack(side=LEFT,padx=10)
pr_ent = Entry(f_top_pro,width=20)
pr_ent.pack(side=LEFT)

f_top_url = LabelFrame(f_ULTRA,text="Введите URL",padx=10,pady=10)
f_top_url.pack(side=LEFT)

Button(f_top_url, text="x",
       command=clean_CIAN).pack(side=LEFT)

Button(f_top_url, text=">>>",
       command=clipboard_CIAN).pack(side=LEFT,padx=5)

ent = Entry(f_top_url,width=40,validatecommand=(root.register(validate), '%P'))
ent.focus_set()
ent.event_add('<<Paste>>', '<Control-Cyrillic_em>')
ent.pack(side=LEFT)


Button(f_top_url, text="Парсим!",
       command=parse_CIANthre).pack(side=RIGHT,padx=10)


f_top = LabelFrame(text="Описание",padx=10,pady=10)
f_top.pack()

text = st.ScrolledText(f_top, wrap=WORD, height = 15)
text.configure(font=("Verdana", 14))
text.pack()

#frame = Frame()
#frame.pack()

#Button(frame, text="Вставить",command=insert_text).pack(side=LEFT)
#Button(frame, text="Взять",command=get_text).pack(side=LEFT)
#Button(frame, text="Удалить",command=delete_text).pack(side=LEFT)

hhent = Entry(width=80)
hhent.pack(pady=10)

fff = Frame()
fff.pack()

f_bot = LabelFrame(fff,padx=10,pady=11)
f_bot.pack(side=LEFT)

fff2 = LabelFrame(fff,text='Цена',padx=10,pady=5,labelanchor='n')
fff2.pack(side=RIGHT)

#l2 = Label(fff2,)
ec = Entry(fff2,width=WDT)
#l2.pack()
ec.pack(pady=5)

textc = st.ScrolledText(fff2,height=6,width=40,wrap=WORD)
textc.configure(font=("Verdana", 12))
textc.pack()


f_bot2 = Frame(f_bot)
f_bot2.pack(side=LEFT)
f_bot3 = Frame(f_bot)
f_bot3.pack(side=RIGHT)

ent1 = Entry(f_bot2,width=WDT)
ent3 = Entry(f_bot2,width=WDT)
ent5 = Entry(f_bot2,width=WDT)
ent7 = Entry(f_bot2,width=WDT)
ent9 = Entry(f_bot2,width=WDT)
ent2 = Entry(f_bot3,width=WDT)
ent4 = Entry(f_bot3,width=WDT)
ent6 = Entry(f_bot3,width=WDT)
ent8 = Entry(f_bot3,width=WDT)
ent10 = Entry(f_bot3,width=WDT)

ent1.pack()
ent2.pack()
ent3.pack()
ent4.pack()
ent5.pack()
ent6.pack()
ent7.pack()
ent8.pack()
ent9.pack()
ent10.pack()

f_topc = Frame()
f_topc.pack(pady=20)

infol = Label(f_topc,text='')
infol.pack()

#Button(f_topc,text="Наложить логотип",command=clean_CIAN).pack(side=RIGHT,padx=20)

Button(f_topc,text="[МАСКА] Создать PDF!",command=crpdfmask).pack(side=LEFT,padx=20)

veryB = Button(f_topc,text="Создать PDF!",command=crpdf)     
veryB.pack(side=RIGHT,padx=10,pady=10)

root.update_idletasks()
s = root.geometry()
s = s.split('+')
s = s[0].split('x')
width_root = int(s[0])
height_root = int(s[1])

w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2
h = h // 2
w = w - width_root // 2
h = h - height_root // 2
root.geometry('+{}+{}'.format(w, h))

root.bind_all("<Key>", _onKeyRelease, "+")
root.mainloop()
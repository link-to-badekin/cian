import requests
import json
from PIL import Image, ImageDraw
import cv2
import os, shutil
import threading


def getphot(lalala):
    start_json_template = "window._cianConfig['frontend-offer-card'] = "
    photos = []
    html = lalala
    if start_json_template in html:
        start = html.index(start_json_template) + len(start_json_template)
        end = html.index('</script>', start)
        json_raw = html[start:end].strip()[:-1]
        json1 = json.loads(json_raw)
        for item in json1:
            if item['key'] == 'defaultState':
                photos.append(item['value']['offerData']['linkToMap'])
                for photo in item['value']['offerData']['offer']['photos']:
                    photos.append(photo['fullUrl'])
                break
    return photos


def downloadphotosss(rows):
    counter = 0
    eblan = []

    os.mkdir('temp/downloaded')
    os.mkdir('temp/processed')
    os.mkdir('temp/noCIAN')
    for i in rows:
        file_name = 'temp/downloaded/i' + str(counter) + '.jpeg'
        #newinf("Скачиваю "+file_name)
        response = requests.get(i)
        file = open(file_name, "wb")
        file.write(response.content)
        file.close()

        threading.Thread(target=jopa,args=(counter,file_name,)).start()

        try:
            #newinf('Обрабатываю i' + str(counter) + '.jpeg')
            photo = Image.open('temp/downloaded/i' + str(counter) + '.jpeg')
            watermark = Image.open('logo.png')
            wi,he = photo.size
            watermark.thumbnail(photo.size)
            w2,h2 = watermark.size
            photo.paste(watermark, (0, (he-h2)//2), watermark)
            photo.save('temp/processed/i' + str(counter) + '.png', "PNG")
            eblan.append((wi,he))
        except Exception:
            pass
        counter += 1
    #newinf('...')
    return eblan
    #downloadmap(rows[-1])



def delall():
    folder = os.path.expanduser('~/Desktop/CIAN/files')
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def jopa(counter,file_name):
    patha = os.path.expanduser('~/Desktop/CIAN/')
    try:
        padwi, padhi = nowater(file_name, patha+'files/noCIAN/' + str(counter) + '.png')
        # newinf('Обрабатываю i' + str(counter) + '.jpeg')
        photo = Image.open(patha+'files/noCIAN/' + str(counter) + '.png')
        watermark = Image.open(patha + 'logo.png')
        wi, he = photo.size
        watermark.thumbnail(photo.size)
        w2, h2 = watermark.size
        #логотип по центру 
        #photo.paste(watermark, (0, (he - h2) // 2), watermark)
        resize_h = 125 
        resize_w = int(resize_h * w2 / h2)
        watermark = watermark.resize((resize_w, resize_h), Image.ANTIALIAS)
        photo.paste(watermark, ( wi - (padwi + 59), he - (padhe + 11) ), watermark)
        # (logo - logo cian)/2 59.5 and 11 
        photo.save(patha + 'files/noCIAN/' + str(counter) + '.png', "PNG")
    except Exception:
        pass


def nowater(imgname,outname):
    patha = os.path.expanduser('~/Desktop/CIAN/')
    # получили фотку циан 
    photo = Image.open(imgname)
    draw = ImageDraw.Draw(photo)
    # объект для рисования 
    draw.rectangle([(0, 0), photo.size], fill=(0, 0, 0))
    watermark = Image.open(patha+'m.png')
    #получили стартовый шаблон лого
    wi, he = photo.size
    #аддаптировали под исходную фотку с циана 
    w2, h2 = watermark.size
    watermark = watermark.resize(( (int(w2*0.9),h2)) ,Image.ANTIALIAS)
    stepright = int(wi/13) 
    stepbottom = int(he/11)
    photo.paste(watermark, (wi - (stepright + w2), he-(stepbottom + h2)), watermark)
    #финальный макет
    photo.save(patha+'m2.png', "PNG")
    img = cv2.imread(imgname)
    mask = cv2.imread(patha+'m2.png', 0)
    # маска плюс исправление
    dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)
    cv2.imwrite(outname, dst)
    return (stepright + w2, stepbottom + h2)


def watermarking():
    patha = os.path.expanduser('~/Desktop/CIAN/')
    counter=-1
    folder = os.path.expanduser('~/Desktop/CIAN/files/downloaded')
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                print(file_path)
                counter = counter + 1
                imgname = file_path
                photo = Image.open(imgname)
                draw = ImageDraw.Draw(photo)
                draw.rectangle([(0, 0), photo.size], fill=(0, 0, 0))
                watermark = Image.open(patha + 'm.png')
                wi, he = photo.size
                watermark.thumbnail(photo.size)
                w2, h2 = watermark.size
                photo.paste(watermark, (0, (he - h2) // 2), watermark)
                photo.save(patha + 'm2.png', "PNG")
                img = cv2.imread(imgname)
                mask = cv2.imread(patha + 'm2.png', 0)
                dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)
                cv2.imwrite(patha+'/processed/'+str(counter)+'.png', dst)
        except Exception as e:
            pass




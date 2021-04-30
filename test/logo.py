






from PIL import Image, ImageDraw
from os import *
import cv2
import numpy 








# получили фотку циан 
name = 'posutochnaja-kvartira-anapa-ulica-lenina-1072422987-1.jpg'
photo = Image.open(name)
draw = ImageDraw.Draw(photo)
    # объект для рисования 
draw.rectangle([(0, 0), photo.size], fill=(0, 0, 0))
print('photo', photo.size)
watermark = Image.open('m.png')
    #получили стартовый шаблон лого
wi, he = photo.size
#watermark.thumbnail( (220,110) )
#аддаптировали под исходную фотку с циана 
w2, h2 = watermark.size
watermark = watermark.resize(( (int(w2*0.9),h2)) ,Image.ANTIALIAS)

stepright = int(wi/13) 
stepbottom = int(he/11)
print('stepright',wi,stepright)
print('stepbottom',he, stepbottom)  
photo.paste(watermark, (wi - (stepright + w2), he-(stepbottom + h2)), watermark)
    #финальный макет he-851)
padwi = stepright + w2
padhe = stepbottom + h2
print(wi - (stepright + w2), he-(stepbottom + h2))

photo.save('m2.png', "PNG")
print(photo.size)
img = cv2.imread(name)
mask = cv2.imread('m2.png', 0)
print(img.shape)
print(mask.shape)
    # маска плюс исправление
dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)
cv2.imwrite('done.jpeg', dst)


photo = Image.open('done.jpeg')
watermark = Image.open('logo.png')
wi, he = photo.size
watermark.thumbnail(photo.size)
w2, h2 = watermark.size
resize_h = 125 
resize_w = int(resize_h * w2 / h2)

watermark = watermark.resize((resize_w, resize_h), Image.ANTIALIAS)
#photo.paste(watermark, (wi - padwi, he-padhe), watermark)

photo.paste(watermark, ( (wi-padwi - 59) , he - padhe - 11 ), watermark)
photo.save( name[0:-3] +'done'+'.png', "PNG")

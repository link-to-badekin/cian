import requests
import os
import re

def find_description(soup):
    result = soup.find('div', attrs = {'data-name':"Description"}).find('p', attrs={'itemprop': "description"})
    plaintext = ' '.join(result.text.split())
    return plaintext

def find_shit(soup):
    result = soup.find('div', attrs = {'data-name':"Description",'id':"description"})
    heh = []
    for each in result.find_all('div', {'class': re.compile(r'--info-title--')}):
        heh.append(each.text)
    for each in result.find_all('div', {'class':re.compile(r'--info-value--')}):
        heh.append(each.text)
    return heh

def find_head(soup):
    result = soup.find('div', attrs = {'data-name':"Geo"})
    return(result.span['content'])

def find_metro(soup):
    result = soup.find('div', attrs={'data-name': "Geo"})
    r = {}
    heh = []
    for each in result.ul:
        heh.append(each.text)
    m = []
    for each in soup.find('div', attrs={'data-name': "Geo"}).findAll('svg', attrs={'data-name': "UndergroundIcon"}):
        m.append(str(each))
    for each in range(0,len(heh)):
        r[heh[each]] = m[each]
    return r

def find_high(soup):
    heh = []
    try:
        for each in soup.find('div', attrs={'data-name': "Geo"}).findAll('li', attrs={'data-name': "renderHighway"}):
            heh.append(each.text)
    except Exception:
        heh = []
    return heh

def find_price(soup):
    return soup.find('div', attrs={'data-name': "OfferCardAside"}).find('span', attrs={'itemprop': "price"})['content']

def processuka(photos_list):
    path_to = os.path.expanduser('~/Desktop/CIAN')
    ashto = photos_list.pop(0)
    temp = ashto.split("center=")[1].split("%2C")
    mapurl = "https://static-maps.yandex.ru/1.x/?ll="+temp[1]+","+temp[0]+"&size=450,450&z=16&l=map&pt="+temp[1]+","+temp[0]+",comma"
    os.mkdir(path_to + '/files/map')
    response = requests.get(mapurl)
    path_to = os.path.expanduser('~/Desktop/CIAN')
    file = open(path_to + '/files/map/map.png', "wb")
    file.write(response.content)
    file.close()



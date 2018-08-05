import json
from time import sleep
from  lxml import html
import requests

def lol(a):
    str=None
    for i in a:
        b=False
        for j in i:
            if(j!=' ' and j!='\n' and j!='\t' ):
                b=True
                break
        str=i
        if b==True:
            break
    if(str!=None):
        str=str.strip()
    else:
        return None
    return str

def amazonparser(url):


    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36'})
    doc = html.fromstring(page.content)
    xpath_name = '//h1[@id="title"]//text()'
    xpath_sale_price = '//span[@id="priceblock_ourprice"]/text()'
    xpath_actual_price = '//div[@id="price"]//span[@class="a-text-strike"]/text() or //div[@id="olp_feature_div"]//span[@class="a-color-price"]/text()'
    xpath_category = '//div[@id="wayfinding-breadcrumbs_container"]//ul//span[@class="a-list-item"]//text()'
    xpath_instock = '//div[@id="availability_feature_div"]//text()'

    raw_name = doc.xpath(xpath_name)
    raw_sale_price = doc.xpath(xpath_sale_price)
    raw_actual_price = doc.xpath(xpath_actual_price)
    raw_category = doc.xpath(xpath_category)
    raw_instock = doc.xpath(xpath_instock)
    raw_name=lol(raw_name)
    raw_sale_price = lol(raw_sale_price)
    if(raw_actual_price==True):
        raw_actual_price=lol(doc.xpath('//div[@id="price"]//span[@class="a-text-strike"]/text()'))
        if raw_actual_price==None:
            raw_actual_price = lol(doc.xpath('//div[@id="olp_feature_div"]//span[@class="a-color-price"]/text()'))
    raw_category=lol(raw_category)
    raw_instock=lol(raw_instock)

    data= {
        'name': raw_name,
        'sale_price': raw_sale_price,
        'actual_price': raw_actual_price,
        'category': raw_category,
        'avaibility': raw_instock,
    }
    return data

ANSI=['B075MHMT4D','B01F1TTLL8','B075MJJDF7','B01GRFGT7E','B01BD7PS2S','B07FF42TFJ','B01N4P95U2'
    ]
extracted_data=[]
for i in ANSI:
    url='https://www.amazon.in/dp/'+i
    print('processing -',url)
    extracted_data.append(amazonparser(url))
    sleep(10)


f=open('data.json','w')
json.dump(extracted_data,f)

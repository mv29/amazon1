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

def amaz2(url):


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

ANSI=[]
def amaz1(url,j):

    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36'})
    doc = html.fromstring(page.content)
    for i in range(j+0,j+30):
        xpath_list = "//li[@id=\"result_"+str(i)+"\"]/@data-asin"
        raw_list=doc.xpath(xpath_list)
        print(raw_list)
        ANSI.append(raw_list)
    j=int(i)-5
    xpath_nextpage = '//a[@id="pagnNextLink"]/@href'
    raw_nextpage = doc.xpath(xpath_nextpage)
    url="https://www.amazon.in"+raw_nextpage[0]
    return [url,j]

products=[]
def amaz3(url,j):

    print("page under processing",url)
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36'})
    if page:
        print("page loaded")
    else:
        print("error in page load")

    doc = html.fromstring(page.content)
    if len(doc)!=0:
        print("html parsed")
    else :
        print("error in html parsing")
    for i in range(j+0,j+30):
        #print(i)
        xpath_src = "//li[@id=\"result_" + str(i) + "\"]//div[contains(@class, 'a-row a-spacing-base')]//div[contains(@class, 'a-section a-spacing-none a-inline-block s-position-relative')]/a/img/@src"
        raw_src = doc.xpath(xpath_src)
        #print(raw_src)
        xpath_name = "//li[@id=\"result_" + str(i) + "\"]//div[contains(@class, 'a-row a-spacing-mini')]//div[contains(@class, 'a-row a-spacing-none')]/a[contains(@class, 'a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal')]/h2/text()"
        raw_name = doc.xpath(xpath_name)
        #print(raw_name)
        xpath_brand = "//li[@id=\"result_" + str(i) + "\"]//div[contains(@class, 'a-row a-spacing-mini')]//div[contains(@class, 'a-row a-spacing-none')][2]/span[contains(@class, 'a-size-small a-color-secondary')][2]/text()"
        raw_brand = doc.xpath(xpath_brand)
        #print(raw_brand)
        xpath_saleprice = "//li[@id=\"result_" + str(i) + "\"]//div[contains(@class, 'a-row a-spacing-mini')]//div[contains(@class, 'a-row a-spacing-none')]/a[contains(@class, 'a-link-normal a-text-normal')]//span[contains(@class, 'a-size-base a-color-price s-price a-text-bold')]/text()"
        raw_saleprice = doc.xpath(xpath_saleprice)
        #print(raw_saleprice)
        xpath_originalprice = "//li[@id=\"result_" + str(i) + "\"]//div[contains(@class, 'a-row a-spacing-mini')]//div[contains(@class, 'a-row a-spacing-none')]/span[contains(@class, 'a-size-small a-color-secondary a-text-strike')]/text()"
        raw_originalprice = doc.xpath(xpath_originalprice)
        #print(raw_originalprice)
        xpath_avaibility = "//li[@id=\"result_" + str(i) + "\"]//div[contains(@class, 'a-row a-spacing-mini')]//div[contains(@class, 'a-row a-spacing-none')]/div[contains(@class, 'a-row a-spacing-none')]//span/text() | //li[@id=\"result_" + str(i) + "\"]//div[contains(@class, 'a-row a-spacing-mini')]//div[contains(@class, 'a-row a-spacing-none')]/div[contains(@class, 'a-row a-spacing-none')]/span[contains(@class, 'a-size-small a-color-price')]/text()"
        raw_avaibiltiy = doc.xpath(xpath_avaibility)
        #print(raw_avaibiltiy)
        xpath_asin = "//li[@id=\"result_" + str(i) + "\"]/@data-asin"
        raw_asin = doc.xpath(xpath_asin)
        if raw_src!=[]:
            if len(raw_avaibiltiy)!=0:
                raw_avaibiltiy='available'
            else:
                raw_avaibiltiy = 'not available'
            if len(raw_originalprice)==0:
                raw_originalprice=raw_saleprice
            products.append([raw_src[0],raw_name[0],raw_brand[0],raw_saleprice,raw_originalprice,raw_avaibiltiy,raw_asin])

    j = int(i) - 5
    xpath_nextpage = '//a[@id="pagnNextLink"]/@href'
    raw_nextpage = doc.xpath(xpath_nextpage)
    url="https://www.amazon.in"+raw_nextpage[0]
    return [url,j]


url1="https://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=phone"

"""
for i in range(1):
    if i==0:
        j=int(0)
        lol1=amaz1(url1,j)
        sleep(10)
        url=lol1[0]
        j = lol1[1]
    print(url,j,)
    url,j = amaz1(url,j)

print(len(ANSI))

extracted_data=[]
for i in ANSI:
    print(i)
    url='https://www.amazon.in/dp/'+i[0]
    print('processing -',url)
    extracted_data.append(amaz2(url))
    sleep(15)


f=open('data.json','w')
json.dump(extracted_data,f)

"""

for i in range(6):
    print("page-",i, "processing")
    if i==0:
        j=int(0)
        lol1=amaz3(url1,j)
        sleep(10)
        url=lol1[0]
        j = lol1[1]
        continue
    url,j = amaz3(url,j)

print(len(products))
#f=open('data.json','w')
#json.dump(products,f)

with open("data.json", "w") as json_file:
    json.dump(products, json_file, indent=4)
    json_file.write("\n")

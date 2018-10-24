import json
from time import sleep
from  lxml import html
import requests
import csv

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

# gathering information of a product by going to product page using asin
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

#gathering the asin number of all products in a page and traversing through pages
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

#gathering the information of all products in a page and traversing through the pages
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



#getting the links for the comments according to their rating for further traversing
def amaz4(url):

    list_comments_url=[]
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

    xpath_5 = '//table[@id="histogramTable"]//a[@title="5 star"]/@href'
    raw_5 = doc.xpath(xpath_5)
    #print(raw_5)
    list_comments_url.append(raw_5[0])

    xpath_4 = '//table[@id="histogramTable"]//a[@title="4 star"]/@href'
    raw_4 = doc.xpath(xpath_4)
    #print(raw_4)
    list_comments_url.append(raw_4[0])

    xpath_3 = '//table[@id="histogramTable"]//a[@title="3 star"]/@href'
    raw_3 = doc.xpath(xpath_3)
    #print(raw_3)
    list_comments_url.append(raw_3[0])

    xpath_2 = '//table[@id="histogramTable"]//a[@title="2 star"]/@href'
    raw_2 = doc.xpath(xpath_2)
    #print(raw_2)
    list_comments_url.append(raw_2[0])

    xpath_1 = '//table[@id="histogramTable"]//a[@title="1 star"]/@href'
    raw_1 = doc.xpath(xpath_1)
    #print(raw_1)
    list_comments_url.append(raw_1[0])

    return list_comments_url


#class for storing the comments and their necessary information
class comments():

    count=0
    def __init__(self, rating,title,name,comment,helpful):
        self.rating =rating
        self.title = title
        self.name=name
        self.comment=comment
        self.helpful=helpful
        comments.count += 1

COMMENTS=[]


# traversing the link of product comment page and traversing to the next page and storing the reqiured information in a list which contains the comment as a object
def amaz5(url,rating):
    print("page under processing", url)

    page = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36'})

    if page:
        print("page loaded")
    else:
        print("error in page load")

    doc = html.fromstring(page.content)

    if len(doc) != 0:
        print("html parsed")
    else:
        print("error in html parsing")

    for i in range(2,12):

        xpath_title = "//div[@id=\"cm_cr-review_list\"]/div[" + str(i)+ "]//div[@class=\"a-row\"]//a[@data-hook=\"review-title\"]/text()"
        raw_title = doc.xpath(xpath_title)
        if len(raw_title)!=0:
            print(raw_title[0])
        else:
            raw_title.append(None)

        xpath_author = "//div[@id=\"cm_cr-review_list\"]/div[" + str(i) + "]//div[@class=\"a-row\"]//a[@data-hook=\"review-author\"]/text()"
        raw_author = doc.xpath(xpath_author)
        if len(raw_author) != 0:
            print(raw_author[0])
        else:
            raw_author.append(None)

        xpath_comment = "//div[@id=\"cm_cr-review_list\"]/div[" + str(i) + "]//div[contains(@class, 'a-row a-spacing-small review-data')]//span[@data-hook=\"review-body\"]/text()"
        raw_comment = doc.xpath(xpath_comment)
        if len(raw_comment) != 0:
            print(raw_comment[0])
        else:
            raw_comment.append(None)

        xpath_help = "//div[@id=\"cm_cr-review_list\"]/div[" + str(i) + "]//div[contains(@class, 'a-row a-expander-container a-expander-inline-container')]//span[@data-hook=\"review-voting-widget\"]//div//span[@data-hook=\"helpful-vote-statement\"]/text()"
        raw_help = doc.xpath(xpath_help)
        helper=[]
        if len(raw_help) != 0:
            helper=raw_help[0].split(' ')
            print(helper[0])
        else:
            helper.append(None)

        COMMENTS.append(comments(rating,raw_title[0],raw_author[0],raw_comment[0],helper[0]))
        print("\n")

    xpath_nextpage = "//div[@id=\"cm_cr-pagination_bar\"]//li[@class=\"a-last\"]/a/@href"
    raw_nextpage = doc.xpath(xpath_nextpage)
    print("\n")
    return raw_nextpage



url1="https://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=phone"



#calling function for amaz1 function
# gathering the asin no of all products in a page and traversing to next page
def mv3():
    for i in range(1):
        if i == 0:
            j = int(0)
            lol1 = amaz1(url1, j)
            sleep(10)
            url = lol1[0]
            j = lol1[1]
        print(url, j, )
        url, j = amaz1(url, j)







# fetching information of a product from a products page and and traversing to the other products in the list
#for loop for amaz2 function
#ANSI list will be generated from mv3
def mv4():
    extracted_data = []
    for i in ANSI:
        print(i)
        url = 'https://www.amazon.in/dp/' + i[0]
        print('processing -', url)
        extracted_data.append(amaz2(url))
        sleep(15)







# fro loop for amaz3 function
# for loop for fetching information of all products in a page and then moving on two next page for further information
def mv1():
    for i in range(6):
        print("page-", i, "processing")
        if i == 0:
            j = int(0)
            lol1 = amaz3(url1, j)
            sleep(10)
            url = lol1[0]
            j = lol1[1]
            continue
        url, j = amaz3(url, j)

    print(len(products))

    with open("data.json", "w") as json_file:
        json.dump(products, json_file, indent=4)
        json_file.write("\n")









# fetching the all the comments of a product and storing them according to the rating
# title,name of author,comment,upvotes of a comment stored
#tested succesfully for 75 pages parsing

def mv2(url):
    lol= amaz4(url)

    for i in range(len(lol)):
        print("processing comments with ratng",5-i," " ,lol[i])
        current_page="https://www.amazon.in"+lol[i]
        for j in range(10):
            next_page = amaz5(current_page, 5 - i)
            sleep(10)
            current_page = "https://www.amazon.in" + next_page[0]
            print(current_page)

    print(len(COMMENTS))
    for i in range(len(COMMENTS)):
        print(COMMENTS[i].rating)
        print(COMMENTS[i].title)
        print(COMMENTS[i].name)
        print(COMMENTS[i].comment)
        print(COMMENTS[i].helpful)

    with open('dob.csv', 'w') as f:
        writer = csv.writer(f)
        for row in COMMENTS:
            mv=[]
            mv.append(row.rating)
            mv.append(row.title)
            mv.append(row.name)
            mv.append(row.comment)
            mv.append(row.helpful)
            writer.writerow(mv)
            mv.clear()



mv2('https://www.amazon.in/dp/B077PWBC6V')

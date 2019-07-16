import smtplib
import re
import requests
from bs4 import BeautifulSoup

#declaring universal variables
isDeal = 0

#initializing
URL = input('Enter the URL of the Amazon Product that you want to check: ')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

def check_price():
    #fetch product title
    global productName
    productName = soup.find(id='productTitle').get_text().strip()

    #fetch product price and convert it to a float type
    global productPrice
    productPrice = soup.find(id='priceblock_ourprice').get_text()
    productPrice = (re.findall('\d+', productPrice))
    productPrice = productPrice[0] + '.' + productPrice[1]
    productPrice = float(productPrice)

    #check if there is a dicounted orice available
    productPriceDeal = soup.find(id='priceblock_dealprice')
    if(productPriceDeal != None):
        global isDeal
        isDeal = 1
        productPriceDeal = productPriceDeal.get_text()
        productPriceDeal = (re.findall('\d+', productPriceDeal))
        productPriceDeal = float(productPriceDeal[0] + '.' + productPriceDeal[1])

    if isDeal == 1:
        productPrice = productPriceDeal

    print('Title: ' +  productName)
    print('Curent Price: $' , productPrice)
    
    global productPriceTarget
    productPriceTarget = float(input('Enter the target price for this product: '))

    if (productPrice <= productPriceTarget):
        send_mail()

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo

    user = 'mailtest123450@gmail.com'
    password = '!Password123'

    reciever = input('Enter the email that you would like to recieve the notification at: ')
    
    server.login(user, password)

    subject = 'The price of ' + productName+ ' has fallen into your set buy range!'
    body = 'Hurry! The price drop may be for a limited time. Buy the product at ' + URL

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(user, reciever, msg)

    print('Email was successfully sent!')

    server.quit()

check_price()

#!/bin/bash
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import csv
import yagmail

# function that will return soup from a url
def get_soup(url="https://stocktwits.com/rankings/watchers"):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.set_page_load_timeout(100)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

def get_data_list(soup):
    # get All of the table row elements
    table_rows = soup.find_all('tr', class_='st_PaKabGw st_1jzr122')
    # for each row get ticker, count of new watches in 24 hours and the price move in 24 hours
    output_data = []
    for i in table_rows:
        ticker = i.find('span', class_='st_3ua_jwB st_8u0ePN3 st_1SuHTwr')  # get ticker by class
        count = i.find_all('td')  # get count of watches as first td tag
        price_move = i.find_all('span')[-1]  # get price move as the last span
        sign = 0

        if len(price_move['class']) < 4:
            sign = 0
        elif price_move['class'][3] == 'st_3ftxMPa':  # identify if pos or neg based on class
            sign = 1
        elif price_move['class'][3] == 'st_16rsg3e':
            sign = -1
        strip_price_move = float(price_move.text.rstrip('%'))
        price_move = sign * strip_price_move
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        #         print(now, " ", ticker.text, " ", count[3].text," ",price_move)
        output_data.append([now, ticker.text, count[3].text, price_move])
    return output_data


def insert_rows(data):
    field_names = ['datetime', 'ticker', 'watchers', 'pricemove']

    for i in data:
        path = "/Users/hugocoussens/git/Winston2.0-Algotrading/DataMining/data/stockwitswatched.csv"
        dict = {"datetime": i[0], "ticker": i[1], "watchers": i[2], "pricemove": i[3], }
        with open(path, 'a') as csv_file:
            dict_object = csv.DictWriter(csv_file, fieldnames=field_names)
            dict_object.writerow(dict)
    print("Record inserted successfully into stocknote table")

if __name__ == "__main__":
    soup = get_soup()
    data = get_data_list(soup)
    insert_rows(data)

    # Send email
    yag = yagmail.SMTP('HCdevelopment22@gmail.com', 'irckrtsyjgkwtbvc')
    contents = ['This is the body, and here is just text http://somedomain/image.png',
                'You can find an audio file attached.']
    yag.send('hbcoussens@gmail.com', 'ScrapeStockwits Successful', data)

    # STDO for log
    print("Successful upload of hot stocks data to sql data base  ", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
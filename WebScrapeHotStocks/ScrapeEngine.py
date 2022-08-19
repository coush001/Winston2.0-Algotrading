from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import mysql.connector


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
        sign=0
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


def get_cursor():
    mydb = mysql.connector.connect(
        host="35.246.42.55",
        user="root",
        password="RF/o<_4eyHm`>&^e"
    )
    mycursor = mydb.cursor()
    mycursor.execute("use stocks")
    return mycursor, mydb


def select_all(mycursor, mydb):
    mycursor.execute("use stocks")
    mycursor.execute("show tables")
    print(mycursor.fetchall())
    mycursor.execute("select * from stocknote")
    print(mycursor.fetchall())
    print('shown all rows')


def drop_all(mycursor, mydb):
    mycursor.execute("use stocks")
    mycursor.execute("delete from stocknote")
    mydb.commit()
    print('deleted all rows')


def insert_rows(data, cursor, connection):
    for i in data:
        mySql_insert_query = """INSERT INTO stocknote (datetime,ticker,watchers,pricechange) 
                            VALUES (%s, %s, %s, %s) """

        record = (i[0], i[1], i[2], i[3])
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Record inserted successfully into stocknote table")

if __name__ == "__main__":
    soup = get_soup()
    data = get_data_list(soup)
    cursor, db = get_cursor()
    # insert_rows(data, cursor, db)
    select_all(cursor, db)
    # drop_all(cursor, db)


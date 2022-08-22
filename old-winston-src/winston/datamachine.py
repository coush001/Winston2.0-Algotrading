import yfinance as yf
from datetime import date, timedelta

class DataAgent():
    """ Data Agent class fetches market data """

    def __init__(self, DaysStart, DaysEnd, symbol):

        self.StartDate = (date.today() + timedelta(days=-DaysStart)).strftime("20%y-%m-%d")
        self.EndDate = (date.today() + timedelta(days=DaysEnd)).strftime("20%y-%m-%d")

        self.Symbol = symbol

        # self.ticker = yf.Ticker(symbol)

        self.data = None

    def fetch(self):
        data = yf.download(self.Symbol, start=self.StartDate, end=self.EndDate)
        return data
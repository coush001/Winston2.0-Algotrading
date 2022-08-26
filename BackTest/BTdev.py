import backtrader as bt
import datetime  # For datetime objects
from swDataConverter import stockwits_converter
print('hello world')

bro = bt.Cerebro()

data = stockwits_converter('../DataMining/stockwitswatched.csv')

bro.adddata(data)
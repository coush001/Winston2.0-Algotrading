from datamachine import DataAgent

class MomentumModel():
    def __init__(self, symbol):
        self.alive = 'yes'
        self.symbol = symbol
        self.Data = None
        self._lookback = 7
        self._end = 0
        self.DataAgent = DataAgent(self._lookback, self._end, self.symbol)

    def get_data(self):
        self.Data = self.DataAgent.fetch()

    def model_output(self):
        self.get_data()
        #print('Index of data:  ', self.Data.index, '\nColumns are:  ', self.Data.columns)
        if self.Data['Open'][-1] > self.Data['Open'].mean(): # If today is higher than last 7 days
            return 1, self.symbol, 10
        elif self.Data['Open'][-1] < self.Data['Open'].mean():
            return 1, self.symbol, 10
        else:
            return 0, self.symbol, 10
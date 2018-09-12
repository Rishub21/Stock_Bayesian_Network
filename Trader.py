
from collections import defaultdict
from create_graph import get_stock_distribution, time_object
import datetime
from Models.Stock_Class import Stock
from Models.Portfolio_Class import Portfolio
import pandas as pd

pd.core.common.is_list_like = pd.api.types.is_list_like

from pandas_datareader import data as pdr
import fix_yahoo_finance as yf

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

yf.pdr_override()

class Trader :

    stock_list = None
    time_object = None

    def __init__(self,stock_list, time_object):
        self.stock_list = stock_list
        self.time_object = time_object

    def back_test(self):
        start = self.time_object.start
        end = self.time_object.end
        interval = self.time_object.interval
        number_time_intervals = (start - end) / interval

        temp_end = start + datetime.timedelta(days=interval) 
        self.__update_stock_prices(str(start), str(temp_end))
        start = temp_end + datetime.timedelta(days=1)


        long_portfolio = Portfolio(self.stock_list) 
        strat_portfolio = Portfolio(self.stock_list) 

        long_portfolio.initialize_holdings() 
        strat_portfolio.initialize_holdings()
        shorts_list = [] 

        while start < end :
            temp_end = start + datetime.timedelta(days=interval) 

            self.__update_stock_prices(str(start), str(temp_end))

            self.trade_and_rebalance(long_portfolio, [])
            self.trade_and_rebalance(strat_portfolio, shorts_list) 
            #strat_portfolio.rebalance_holdings(shorts_list) 

            shorts_list = self.generate_shorts() 
            strat_portfolio.conduct_shortings(shorts_list) 

            start = temp_end + datetime.timedelta(days=1)

        print ("LONG SHARPE " + str(long_portfolio.get_sharpe_ratio()))
        print(long_portfolio.portfolio_return_each_week_list)
        print ("STRAT SHARPE " + str(strat_portfolio.get_sharpe_ratio()))
        print(strat_portfolio.portfolio_return_each_week_list)

        self.graph(strat_portfolio.week_number_list, strat_portfolio.portfolio_val_each_week_list,long_portfolio.portfolio_val_each_week_list)

    def graph(self, time_period, strat_returns, long_returns): 
        plt.plot(time_period, strat_returns, color='blue')
        plt.plot(time_period, long_returns, color='orange')
        plt.xlabel('Weeks')
        plt.ylabel('Portfolio value')
        plt.title('Strat vs Long Only June 2017 - Jan 2018')
        plt.legend()
        plt.show()

    
    def trade_and_rebalance(self, portfolio, shorts_list ): 
        portfolio.add_periodic_value()

        if(len(shorts_list) > 0):
            portfolio.rebalance_holdings(shorts_list)

    def generate_shorts(self):
        self.__mark_stocks_up_or_down() 
        shorts_list = []
        for stock in self.stock_list:
            if(stock.current_status == "up"):
                shorts_list = shorts_list + self.__find_shorts_for_specific_stock(stock.child_probabilities_when_parent_up_dict)
            if(stock.current_status == "down"):
                shorts_list = shorts_list + self.__find_shorts_for_specific_stock(stock.child_probabilities_when_parent_down_dict)
        return set(shorts_list)

    def __find_shorts_for_specific_stock(self,child_probabilities_dictionary):
        short_list = []
        for child in child_probabilities_dictionary:
            #print(child_probabilities_dictionary[child][0])
            if(child_probabilities_dictionary[child][0] <= -.08): # TODO : change this benchmark  
                short_list.append(child)
        return short_list  

    def __mark_stocks_up_or_down(self):
        stock_direction_dictionary = defaultdict(Stock)
        for stock in self.stock_list:
            if(stock.price_list[-1] > stock.price_list[0]):
                stock.current_status = "up"
            else:
                stock.current_status = "down"

    def __update_stock_prices(self, start_period, end_period): 
        for stock in self.stock_list: 
            stock.price_list =  pdr.get_data_yahoo(stock.name, start = start_period, end = end_period)["Close"] 
            stock.last_closing_price = stock.price_list[-1]


if __name__ == "__main__":

    start = datetime.date(year= 2017,day=01,month=01)
    end = datetime.date(year= 2018,day=30,month=12)  

    learning_time_object = time_object(start,end, 7)
    stock_list = get_stock_distribution("Sample_Portfolios/utility_tickers.txt", learning_time_object)

    start = datetime.date(year= 2018,day=1,month=01)
    end = datetime.date(year= 2018,day=30,month=06)

    testing_time_object  = time_object(start,end, 7)
    trader = Trader(stock_list, testing_time_object)
    trader.back_test()

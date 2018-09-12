"""
1) Get tickers
2) Get price data for each ticker
3) Compute the probability given that certain stock went up in one week, the others did the next week
"""
from collections import defaultdict
from Models.Stock_Class import Stock
from Models.Stock_Compare_Class import Stock_Comparator
import pandas as pd

pd.core.common.is_list_like = pd.api.types.is_list_like

from pandas_datareader import data as pdr
import fix_yahoo_finance as yf

yf.pdr_override()

def get_stock_distribution(file, time_object):
    stock_list = get_stock_list(file, time_object)
    time_interval = time_object.interval
    for parent_stock in stock_list:
        populate_stock_distribution(parent_stock, parent_stock)
        for child_stock in stock_list:
            if(child_stock != parent_stock):
                populate_stock_distribution(parent_stock, child_stock)

    #print ("*************************")
    #print_stock_list(stock_list)
    return stock_list


def populate_stock_distribution(parent_stock, child_stock):
    stock_compare = Stock_Comparator(parent_stock, child_stock)

    probability_child_going_up_given_parent_up = stock_compare.get_bayesian_probability_child_up_given_parent_up()
    parent_stock.child_probabilities_when_parent_up_dict[child_stock] = [probability_child_going_up_given_parent_up  - child_stock.get_probability_up()]

    probability_child_going_up_given_parent_down = stock_compare.get_bayesian_probability_child_up_given_parent_down()
    parent_stock.child_probabilities_when_parent_down_dict[child_stock] = [(probability_child_going_up_given_parent_down - child_stock.get_probability_up())]

def get_stock_list(file, time_object):
    stock_list = []
    ticker_list = get_ticker_list(file)

    for ticker in ticker_list:
        new_stock = Stock(ticker, time_object.interval)
        new_stock.price_list = get_price_series_of_ticker(ticker, time_object)
        stock_list.append(new_stock)
    return stock_list
    # create dictionary that maps each stock to its price series
def get_ticker_list(file):
    ticker_list = []
    with open(file, "r") as ticker_file:
        for line in ticker_file:
            ticker_list.append(line.strip())
    return ticker_list

def get_price_series_of_ticker(ticker, time_object):
    data = pdr.get_data_yahoo(ticker, start = time_object.start, end= time_object.end)["Close"]
    return data

def print_stock_list(stock_list):
    for stock in stock_list:
        print ("PARENT " + stock.name)
        for child in stock.child_probabilities_when_parent_up_dict:
            print(child.name)
            print((stock.child_probabilities_when_parent_up_dict[child]))

class time_object:
    start = None
    end = None
    interval = None
    def __init__(self,start,end,interval):
        self.start = start;
        self.end = end
        self.interval = interval

if __name__ == "__main__":
    #list = get_ticker_list("tickers.txt")
    time_object = time_object("2013-01-01","2017-04-30", 7)
    stock_list = get_stock_list("tickers.txt", time_object)
    get_stock_distribution("tickers.txt", time_object)
   # print (stock_list[0].child_probabilities_when_parent_up_dict)
    #create_joint_distribution("tickers.txt", time_object)

    # pick smaller time intervals so larger sample size
    # also if you pick large time intervals you might be capturing something more of a trend then actual thing

    #data = get_stock_list("tickers.txt", time_object)
    #print data[0].get_probability_up_with_child(7, data[1])
    #print data[0].get_probability_up(7)
    #print data[0].get_bayesian_probability(7, data[1])
    #print(data[0].get_total_up_periods_with_child(7, data[1]))

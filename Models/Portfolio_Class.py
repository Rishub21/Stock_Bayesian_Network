from Stock_Class import Stock 
from collections import defaultdict
import numpy as np

class Portfolio: 

    def __init__(self, stock_list): 
        self.starting_val = 10000
        self.cash_holdings = 10000
        self.holdings_map = defaultdict(Stock)
        self.portfolio_val_each_week_list = [self.starting_val]
        self.portfolio_return_each_week_list = [0]
        self.stock_list = stock_list 
        self.week_number_list  = [1] 


    def initialize_holdings(self): 
        self.__generate_holdings(self.stock_list)
        
    def add_periodic_value(self): 
        self.week_number_list.append(len(self.week_number_list) + 1)
        sum = self.cash_holdings
        for stock in self.holdings_map: 
            sum += stock.last_closing_price * self.holdings_map[stock] 

        return_for_week = self.__get_return(sum)
        self.portfolio_return_each_week_list.append(return_for_week)    
        self.portfolio_val_each_week_list.append(sum)
        print ("THE VALUE AFTER TRADE IS " + str(sum) + "with " + str(self.cash_holdings) )
    
    def rebalance_holdings(self, short_list): 
        self.__generate_holdings(short_list)
    
    def conduct_shortings(self, short_list): 
        for stock in short_list: 
            current_num_shares = self.holdings_map[stock] 
            print("SHORTED " + str(current_num_shares) + " of " + str(stock.name) + " at " + str(stock.last_closing_price))
            print ("should get this much val " + str(current_num_shares * stock.last_closing_price))
            self.cash_holdings += (current_num_shares * stock.last_closing_price)
            self.holdings_map[stock] = 0
    
    def get_sharpe_ratio(self): 
        return self.__get_mean_of_returns() / self.__get_standard_deviation_of_returns()
    
    def __get_mean_of_returns(self): 
        return np.mean(self.portfolio_return_each_week_list) 

    def __get_standard_deviation_of_returns(self): 
        return np.std(self.portfolio_return_each_week_list)

    def __get_return(self, sum): 
        return (sum - self.portfolio_val_each_week_list[-1]) / self.portfolio_val_each_week_list[-1]
  
    def __generate_holdings(self, stock_list): # where stock_list is either all stocks for initialization or just the short list for rebalance
        cash_for_each_stock = self.cash_holdings / len(stock_list)
        print("CASH ON HAND FOR REBALNCING " +  str(self.cash_holdings))
        print ("NUMBER OF STOCKS TO SHORT " + str(len(stock_list)))
        print ("Cash for each stock" + str(cash_for_each_stock))
        self.cash_holdings = 0 
        for stock in stock_list: 
            num_shares_to_purchase = int(cash_for_each_stock / stock.last_closing_price)
            print ("PURCHASING " + str(num_shares_to_purchase) + " of " + str(stock.name) + " at " + str(stock.last_closing_price))
            self.holdings_map[stock] = num_shares_to_purchase 
            self.cash_holdings += cash_for_each_stock - (num_shares_to_purchase * stock.last_closing_price)

    


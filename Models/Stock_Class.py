from collections import defaultdict

class Stock :
    price_list = None
    last_closing_price = None
    child_probabilities_when_parent_up_dict = None
    child_probabilities_when_parent_down_dict = None
    time_interval = None
    current_status = None
    
    def __init__(self, name, time_interval):
        self.name = name
        self.child_probabilities_when_parent_up_dict = defaultdict(Stock)
        self.child_probabilities_when_parent_down_dict = defaultdict(Stock)
        self.time_interval = time_interval
    
    def __str__(self): 
        return self.name 

    def get_probability_up(self):
            return (float(self.__get_total_up_periods())/ self.get_total_periods())

    def get_probability_down(self):
            return (float(self.__get_total_down_periods())/ self.get_total_periods())


    def __get_total_up_periods(self):
        total_up_periods = 0
        time_interval = self.time_interval
        for period_number in range(self.get_total_periods() - 1) :
            if(self.price_list[time_interval * (period_number + 1)] > self.price_list[time_interval * (period_number)]):
                total_up_periods += 1
        return total_up_periods

    def __get_total_down_periods(self):
        total_up_periods = 0
        time_interval = self.time_interval
        for period_number in range(self.get_total_periods() - 1) :
            if(self.price_list[time_interval * (period_number + 1)] < self.price_list[time_interval * (period_number)]):
                total_up_periods += 1
        return total_up_periods

    def get_total_periods(self):
        return (len(self.price_list)) / (self.time_interval)

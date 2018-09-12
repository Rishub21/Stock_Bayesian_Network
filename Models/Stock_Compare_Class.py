from scipy.special import comb

class Stock_Comparator :
    parent_stock = None
    child_stock = None
    time_interval = None

    def __init__(self, parent_stock, child_stock):
        self.parent_stock = parent_stock
        self.child_stock = child_stock
        self.time_interval = self.parent_stock.time_interval

    def get_bayesian_probability_child_up_given_parent_up(self): # using bayes formula
        return (self.get_probability_child_up_and_parent_up() / self.parent_stock.get_probability_up())

    def get_bayesian_probability_child_up_given_parent_down(self):
        return (self.get_probability_child_up_and_parent_down() / self.parent_stock.get_probability_down())


    def get_probability_child_up_and_parent_up(self):
        return (float(self.get_total_periods_child_up_and_parent_up()) / self.get_total_periods())

    def get_probability_child_up_and_parent_down(self):
        return (float(self.get_total_periods_child_up_parent_down()) / self.get_total_periods())

    def get_total_periods_child_up_and_parent_up(self):
        total_union_up_periods = 0
        for period_number in range(self.get_total_periods() - 2):
            if(self.parent_stock.price_list[self.time_interval * (period_number + 1)] > self.parent_stock.price_list[self.time_interval * (period_number)]):
                if(self.child_stock.price_list[self.time_interval * (period_number + 2)] > self.child_stock.price_list[self.time_interval * (period_number + 1)]):
                    total_union_up_periods += 1
        return total_union_up_periods

    def get_total_periods_child_up_parent_down(self):
        total_union_up_periods = 0
        for period_number in range(self.get_total_periods() - 2):
            if(self.parent_stock.price_list[self.time_interval * (period_number + 1)] < self.parent_stock.price_list[self.time_interval * (period_number)]):
                if(self.child_stock.price_list[self.time_interval * (period_number + 2)] > self.child_stock.price_list[self.time_interval * (period_number + 1)]):
                    total_union_up_periods += 1
        return total_union_up_periods

    def get_total_periods(self):
        return min(self.parent_stock.get_total_periods(), self.child_stock.get_total_periods())


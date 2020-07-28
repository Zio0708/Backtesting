import sqlite3
import pandas as pd
import Db

class Algo_test01:
    def __init__(self,scope):
        # self.last_day_high
        # self.last_day_low
        # self.now_day_start
        # self.now_day_price
        self.scope=scope

    def cal_sell(self,now_price,price_range,start_price):
        target_price = start_price + (price_range*self.scope)
        if now_price >= target_price:
            return True
        else:
            return False


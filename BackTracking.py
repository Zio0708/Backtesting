import sqlite3
import pandas as pd
import Db

NO_CHANGE = 0  # 이번 minute에 아무 행동 안 함
CHANGE = 1  # 이번 minute에 매수하거나 매도함

BUY_REASON = "VAR1과 VAR2 때문에 매수"
SELL_REASON_VAR1 = "VAR1 때문에 매도"
SELL_REASON_VAR2 = "VAR2 때문에 매도"


class OrderBacktracking:
    def __init__(self, var1, var2):
        self.db = Db.StockDb()
        self.change = NO_CHANGE
        self.reason = ""
        self.var1 = var1
        self.var2 = var2

    def _init_by_day(self):
        self.buy_list = pd.DataFrame(columns=('date', 'buy_price', 'reason'))
        self.sell_list = pd.DataFrame(columns=('date', 'sell_price', 'reason'))
        self.order_id = 0
        self.order = False  # False : 가진 주식 없음, True : 가진 주식 있음

    def set_day(self, day):
        self.day = day
        self.daily_data = self.db.select_MinuteData(day)
        self.daily_start = self.db.select_DailyStart(day)
        self._init_by_day()
        self._order_history()

    def set_var1_and_var2(self, var1, var2):
        if (self.var1 == var1 and self.var2 == var2):
            return
        self.db.delete_Buy_Sell()
        self.var1 = var1
        self.var2 = var2
        self._init_by_day()

        ....알고리즘
        매수, 매도
        관련
        함수

    def _order_history(self):
        if (self.is_order_data()):
            return

        data_len = len(self.daily_data) - 1  # 3시 20분에서 3시 30분 제외

        for i in range(data_len):


            if self.change == CHANGE:
                if self.order:
                    data = self.buy_list.ix[self.order_id]
                    self.db.insert_Buy(data['date'], data['buy_price'], data['reason'])
                else:
                    data = self.sell_list.ix[self.order_id]
                    self.db.insert_Sell(data['date'], data['sell_price'], data['reason'])
                    self.order_id += 1
                self.change = NO_CHANGE

        if self.order:
            price = self.daily_data['high'][data_len - 1]
            date = self.daily_data['date'][data_len - 1]
            self.sell_list = self.sell_list.append(pd.Series({'date': date, 'sell_price': price, 'reason': "당일 종가"}),
                                                   ignore_index=True)
            self.db.insert_Sell(date, int(price), "당일 종가")

        self.db.commit()

    def cal_profit(self):
        self.profit = 1
        buy_len = len(self.buy_list)
        for i in range(len(self.buy_list)):
            self.profit = self.profit * self.sell_list['sell_price'][i] / self.buy_list['buy_price'][i] * 0.9997
        return self.profit

    def is_order_data(self):
        self.buy_list = self.db.select_Buy(self.day)
        if len(self.buy_list) == 0:
            return False
        else:
            self.sell_list = self.db.select_Sell(self.day)
            return True

    def get_day_profit(self, day):
        self.set_day(day)
        profit = self.cal_profit()
        self.print_Profit(day, profit)
        return profit

    def get_days_profit(self, start, end):
        date_data = self.db.select_Date(start, end)
        date_len = len(date_data)
        self.profit_datas = pd.DataFrame(columns=('date', 'profit', 'total_profit'))
        total_profit = 1
        if date_len == 0:
            print("두 날짜 사이의 거래일이 없음")
        for i in range(date_len):
            day = date_data['date'][i][0:8]
            self.set_day(day) #당일 수익률 계산
            profit = self.cal_profit()
            total_profit *= profit
            self.profit_datas = self.profit_datas.append(
                pd.Series({'date': day, 'profit': profit, 'total_profit': total_profit}), ignore_index=True)
        self.print_Total_Profit(day, total_profit)
        return self.profit_datas

    def print_Profit(self, day, profit):
        profit = (profit - 1) * 100
        print(str(day) + " 수익률 : " + str(profit))

    def print_Total_Profit(self, day, profit):
        profit = (profit - 1) * 100
        print(str(day) + " 총 수익률 : " + str(profit))


if __name__ == "__main__":
    main = OrderBacktracking()
    main.get_days_profit("20200203", "20200715")

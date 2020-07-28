import Algo_test01
import Db
import pandas as pd
class BackTradeTest:
    def __init__(self):
        self.algo = Algo_test01.Algo_test01(0.5)
        self.db = Db.StockDb()

    def day_setting(self,start,end):
        date_data = self.db.select_Date(start, end)
        date_len = len(date_data)
        print(len(date_data))
        # self.profit_datas = pd.DataFrame(columns=('date', 'profit', 'total_profit'))
        self.total_profit = 1
        # if date_len == 0:
        #     print("두 날짜 사이의 거래일이 없음")
        for date in range(date_len-1):
            if (date!=0) :
                self.total_profit *= self.day_trading(date_data,date)
                print("%f %s" % (self.total_profit, date))


        print("%d일 동안의 총 수익률 : %f프로" %(date_len,(self.total_profit-1)*100))

    def day_trading(self,date_data,date):
        day = date_data['date'][date][0:8]
        last_day = date_data['date'][date - 1][0:8]
        next_day = date_data['date'][date + 1][0:8]
        self.daily_data = self.db.select_MinuteData(day)
        self.next_day_data = self.db.select_Daily_Data(next_day)
        self.last_day_data = self.db.select_Daily_Data(last_day)

        high = self.last_day_data['high']
        low = self.last_day_data['low']
        price_range = int(high)-int(low)
        start_price = self.daily_data['now'][0]
        next_start_price = self.next_day_data['start']
        daliy_min_len = len(self.daily_data) - 1  # 3시 20분에서 3시 30분 제외

        for min in range(daliy_min_len):
            now_price = self.daily_data['now'][min]
            if self.algo.cal_sell(now_price,price_range,start_price):
                #profit  = int(self.daily_data['now'][daliy_min_len]) - int(self.daily_data['now'][min])
                profit = int(next_start_price) / int(self.daily_data['now'][min])*0.995
                print("%f %s" %(profit,day))
                return profit

        return 1

if __name__ == "__main__":
    main = BackTradeTest()
    main.day_setting("20200217", "20200721")
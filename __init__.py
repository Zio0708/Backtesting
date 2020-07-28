from github.Stock import *
import sys
from PyQt5.QtWidgets import *
class Main():
    def __init__(self):
        self.app = QApplication(sys.argv)
        # self.kiwoom = Kiwoom()
        # self.kiwoom.setWindowTitle("단타매매 프로그램")
        # self.kiwoom.resize(2000,600)
        # self.kiwoom.show()
        # self.app.exec_()
        self.stock = Stock()
        self.stock.comm_connect()
        self.stock.req_minute_data()
        self.stock.req_day_data()
if __name__ == "__main__":
    Main()
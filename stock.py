import os
import csv
import time
import openpyxl
import numpy as np
import tushare as ts
from math import floor
from pandas.io.parsers import read_csv
from concurrent.futures import ThreadPoolExecutor,  as_completed

from tushare import stock


def partition(ls, size):
    """
    Returns a new list with elements
    of which is a list of certain size.

        >>> partition([1, 2, 3, 4], 3)
        [[1, 2, 3], [4]]
    """
    return [ls[i:i+size] for i in range(0, len(ls), size)]


class Stock:
    def __init__(self) -> None:
        super().__init__()

        array = [100*n for n in range(1,2)]
        array.append(50)
        self.array = array
        ts.set_token('e0971dcf036c61bd699ac86762b33d9e6d44025979ac91f6dfc58b31')
        self.pro = ts.pro_api()
        # data = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        # data.to_excel('stock.xlsx')
        self.pool = ThreadPoolExecutor(128)
        self.price = list()
        self.result = list()



    def read_csv(self):
        csv_file = open('stock.csv', 'r', encoding='UTF-8')
        reader = csv.reader(csv_file)

        data = []
        dic_name = dict()
        for item in reader:
            if reader.line_num == 1:
                continue
            data.append(item[1])
            dic_name[item[1]] = item[3]

        csv_file.close()
        self.data = data
        self.dic_name = dic_name
        

    def find_nearest(self, value):
        array = np.asarray(self.array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]


    def daily(self,ts_code):
        date = '20210121'
        df = self.pro.daily(ts_code=ts_code, start_date=date, end_date=date)
        # print(df.to_dict())

        # print(df)
        return df



    def all(self):
        n = 50
        i=0
        res = partition(self.data, floor(len(self.data)/n))
        for item in res:
            i = i+1
            print("all:", str(i))
            df = self.daily(','.join(item))
            self.calcualte(df)
        

    def calcualte(self, df):  
        for value, ts_code, change in zip(df.high, df.ts_code, df.change):
            try:
                # print(ts_code, value)
                near_value = self.find_nearest(value)
                if value>=near_value*0.93 and value<=near_value*1.07:
                    if change > 0:
                        self.result.append(ts_code)
            except:
                pass

            
        # print(self.result)


    def add_name(self):
        openpyxl.load_workbook('stock.xlsx')
        stock_wb =  openpyxl.load_workbook(filename = 'stock.xlsx')
        stock_source = stock_wb['Sheet1']
        dic = dict()
        for row in range(1,stock_source.max_row):
            key = stock_source.cell(row=row, column=2).value
            value = stock_source.cell(row=row, column=4).value
            dic[key] = value

        
        daily_wb = openpyxl.load_workbook(filename='0.xlsx')
        daily_source = daily_wb['Sheet1']
        for row in range(2, 65):
            key = daily_source.cell(row=row, column=2).value
            daily_source.cell(row=row, column=13, value=dic[key])

        daily_wb.save(filename='0.xlsx')   

        



def run():

    time_start = time.time()

    stock = Stock()
    # stock.read_csv()
    # stock.all()
    # print('len: ' + str(len(stock.result)))
    # num = floor(len(stock.result)/100)+1
    # res = partition(stock.result, floor(len(stock.result)/num))
    # for i, item in zip(range(num),res):
    #     df = stock.daily(','.join(item))
    #     df.to_excel(str(i)+'.xlsx')

    stock.add_name()
    
    
    time_end = time.time()
    print('time cost', time_end-time_start, 's')

    print('finish')
    # os.system('pause')


run()

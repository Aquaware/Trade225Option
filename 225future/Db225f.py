# -*- coding: utf-8 -*-
import sys
sys.path.append("../common")

import pandas as pd

import pytz
from datetime import datetime
from Postgres import Postgres, Structure
from CalendarTime import Now, DeltaHour
from CalendarTime import toNaive
from Timeframe import Timeframe




TIME = 'time'
OPEN = 'open'
HIGH = 'high'
LOW = 'low'
CLOSE = 'close'
VOLUME = 'volume'



TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
MANAGE_TABLE_NAME = 'manage'

DB_NAME = 'NK225F'
DB_USER = 'postgres'
DB_PASSWORD = 'bxkxbxn'
DB_PORT = '5432'

def PriceTable(timeframe_str):
    struct = {TIME: 'timestamp', OPEN: 'real', HIGH: 'real', LOW:'real', CLOSE: 'real', VOLUME:'int'}
    table = Structure(timeframe_str, [TIME], struct)
    return table

class Db225f(Postgres):
    
    def __init__(self):
        super().__init__(DB_NAME, DB_USER, DB_PASSWORD, DB_PORT)
        pass
    
    def insertPrices(self, timeframe, prices):
        table = PriceTable(timeframe.symbol)
        is_table = self.isTable(table.name)
        if  is_table == False:
            self.create(table)
        self.insert(table, prices)
        return  

    def fetchItem(self, table, where=None):
        array = self.fetch(table, where)
        return self.value2dic(table, array)

    def fetchAllItem(self, table, asc_order_column):
        array = self.fetchAll(table, asc_order_column)
        return self.values2dic(table, array)
 
    def value2dic(self, table, values):
        dic = {}
        if len(values) == 0:
            return dic
        for (column, value) in zip(table.all_columns, values[0]):
            if table.typeOf(column) == 'timestamp':
                t1 = value.astimezone(pytz.timezone('Asia/Tokyo'))
                dic[column] = t1
            else:
                dic[column] = value
        return dic
    
    def values2dic(self, table, values):
        dic = {}
        for i in range(len(table.columns)):
            column = table.columns[i]
            d = []
            for v in values:
                d.append(v[i])
            if table.typeOf(column) == 'timestamp':
                dic[column] = self.time2pyTime(d)
            else:
                dic[column] = d
        return dic
    
    
    def queryPrice(self, timeframe, begin_time, end_time):
        table = PriceTable(timeframe.symbol)
     
        if begin_time is not None:
            where1 = TIME + " >= cast('" + str(begin_time) + "' as timestamp) "
        else:
            where1 = ''
        if end_time is not None:
            where2 = TIME + " <= cast('" + str(begin_time) + "' as timestamp) "
        else:
            where2 = ''

        if begin_time is not None and end_time is not None:
            where = ''
        else:
            where = where1 + where2
            
        items = self.fetchItemsWhere(table, where, TIME)
        time = []
        values = []
        for item in items:
            time.append(toNaive(item[0]))
            v = item[3]
            values.append([v, v, v, v, item[4]])
        return TimeSeries(time, values, OHLCV)
        
# ----

def build():
    db = Db225f()
    if db.isTable(MANAGE_TABLE_NAME) == False:
        table = ManageTable()
        db.create(table)
        

def importFromCsv():
    import glob
    files = glob.glob("./data/*.csv")

    values = []
    for file in files:
        df = pd.read_csv(file, encoding='SJIS')
        df['時刻'] = df['日付'] + ' ' + df['時間']
        df1 = df[['時刻', '始値', '高値', '安値', '終値', '出来高']]
        value = df1.to_numpy().tolist()
        values += value
    
    data = []
    for time_str, open, high, low, close, volume in values:
        t = datetime.strptime(time_str, "%Y/%m/%d %H:%M")
        data.append([t, open, high, low, close, volume])
        
    sorted_data = sorted(data, key=lambda s: s[0]) 

    db = Db225f()
    timeframe = Timeframe('M1')
    db.insertPrices(timeframe, sorted_data)
    print('Data imported  ', len(sorted_data) )
    
    
if __name__ == '__main__':
    #build()
    importFromCsv()
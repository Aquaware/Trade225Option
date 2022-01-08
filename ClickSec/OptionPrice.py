# -*- coding: utf-8 -*-

from CalendarTime import Now, DeltaDay
import datetime


def importFromTable(contract_month, table):
    prices = []
    for row in table:
        if len(row) != 27:
            continue
        try:
            # Call
            kind = 'C'
            contract_price = int(row[13])
            iv = float(row[0])
            theta = float(row[1])
            vega = float(row[2])
            delta = float(row[4])
            gamma = float(row[5])
            volume = int(row[9])
            price = float(row[11])
            time = parseTime(row[12])
            p = OptionPrice(time, contract_month, contract_price, kind, price, volume, delta, gamma, theta, vega, iv)
            prices.append(p)
        except:
            dummy = 1
        
        try:
            # Put
            kind = 'P'
            contract_price = int(row[13])
            price = float(row[14])
            time = parseTime(row[15])
            volume = int(row[17])
            delta = float(row[21])
            gamma = float(row[22])
            iv = float(row[23])
            theta = float(row[24])
            vega = float(row[25])
            p = OptionPrice(time, contract_month, contract_price, kind, price, volume, delta, gamma, theta, vega, iv)
            prices.append(p)
        except:
            continue
        
    return prices
        
def parseTime(time_str):
    values = time_str.split(':')
    if len(values) != 2:
        return None
    hour = int(values[0])
    minutes = int(values[1])
    now = Now()
    y = now.year
    m = now.month
    d = now.day
    time = datetime.datetime(y, m, d, hour, minutes)
    if time > now:
        time -= DeltaDay(1)
    return time
        
        
class OptionPrice():
    
    def __init__(self, time, contract_month, contract_price, kind, price, volume, delta, gamma, iv, theta, vega):
        self.time = time
        self.contract_month = contract_month
        self.contract_price = contract_price 
        self.kind = kind
        self.price = price
        self.volume = volume
        self.delta = delta
        self.gamma = gamma
        self.iv = iv
        self.theta = theta
        self.vega = vega
        return
    
    def description(self):
        print(self.time, self.contract_month, self.contract_price, self.kind, self.price, self.volume)
    

        
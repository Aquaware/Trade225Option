#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 21:58:49 2018

@author: iku
"""
import os
import sys
current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir + "/../common")
sys.path.append(current_dir + "/../private")

import threading
from ChromeHandler import ChromeHandler
import OptionParser
from OptionDb import OptionDb, TickTable
from OptionPrice import importFromTable

from datetime import datetime, timedelta
import time

from CalendarTime import Today, DeltaMonth
from Timer import Timer


chrome = ChromeHandler()

CLICK_SEC_URL = "https://sec-sso.click-sec.com/loginweb/"
CLICK_SEC_ID = "xxxxxxxxx"
CLICK_SEC_PW = "ik8xxxxxx"

intervalSec = 0.1
timer1 = None
timer2 = None

def now():
    return datetime.now()

class EveryMinutesTimer(object):
    
    def __init__(self, minutes):
        t = now()
        tnext = datetime(t.year, t.month, t.day, t.hour)
        self.minutes = minutes
        while tnext < t:
            tnext += timedelta(minutes=minutes)
        self.next_time = tnext
        
    def shouldDo(self):
        t = now()
        if t >= self.next_time:
            self.next_time += timedelta(minutes=self.minutes)
            return True
        else:
            return False
        
class EveryDayTimer(object):
    def __init__(self, hour, minute):
        t = now()
        self.hour = hour
        self.minute = minute        
        tnext = datetime(t.year, t.month, t.day) + timedelta(days=1)
        tnext += timedelta(hours=hour)
        tnext += timedelta(minutes=minute)
        self.next_time = tnext
        
    def shouldDo(self):
        t = now()
        if t >= self.next_time:
            tnext = datetime(t.year, t.month, t.day) + timedelta(days=1)
            tnext += timedelta(hours=self.hour)
            tnext += timedelta(minutes=self.minute)
            self.next_time = tnext
            return True
        else:
            return False    
    
class TickBuffer(object):
    def __init__(self, name):
        self.name = name
        self.buffer = []
        self.date = None
        
    def add(self, tick_list):
        if tick_list is None:
            print('error in add method')
            return None
        if len(tick_list) == 0:
            print('error in add method')
            return None
        
        tick = tick_list[-1]
        t = tick[0]
        out = None
        if self.date is None:
            self.date = datetime(t.year, t.month, 1)
        for tick in tick_list:
            [t, bid, ask] = tick
            if t.year > self.date.year or t.month > self.date.month:
                out = self.buffer.copy()
                self.buffer = []
                self.date = datetime(t.year, t.month, 1)
            self.buffer.append([t, bid, ask, (bid + ask) / 2, 0])
            
        return out
         
    def flush(self):
        out = self.buffer.copy()
        self.buffer = []
        self.date = None
        return out
    
def int2str(d, length):
    s = '0000' + str(d)
    n = len(s)
    return s[n - length: n]

def contractCode():
    t = Today()
    code = []
    for i in range(4):
        y = int2str(t.year, 4)
        m = int2str(t.month, 2)
        code.append(y + m)
        t += DeltaMonth(1)
         
    #"202178">2021/12/17限月
    #"202179">2021/12/24限月
    #"202180">2021/12/30限月
    #"202240">2022/01/07限月
    code.append('202241')
    code.append('202242')
    code.append('202243')
    
    print(contractCode)
    return code 

def getOptionPrices():
    codes = contractCode()
    for code in codes:
        try:
            chrome.selectListByName('targetDeliveryMonth', code)
            chrome.executeJS("changeDeliveryMonth('0')", [])
            getOptionPrice(code)
        except:
            continue
        
def getOptionPrice(theMonth):
    chrome.clickButtonByName('reloadButton')
    parser = OptionParser.OptionParser(chrome.html())
    prices = parser.parse(theMonth)
    db = OptionDb()
    for price in prices:
        price.description()   
    db.updatePrices(prices)
    return
   
def close():
    chrome.close()
    pass

def login():
    chrome.connect(CLICK_SEC_URL)
    time.sleep(5)
    chrome.inputElement("j_username", CLICK_SEC_ID)
    chrome.inputElement("j_password", CLICK_SEC_PW)
    chrome.clickButtonByName("LoginForm")
    chrome.linkByClassName("js-fuop")
    chrome.linkByText("オプション注文")
    return

def GMONavigator():
    scrape()
    
def scrape():
    login()
    timer2 = Timer(2.0, getOptionPrices)
    timer2.run()
    
    pass

def test():
    login()
    getOptionPrices()
    

if __name__ == "__main__":
    scrape()
    #test()

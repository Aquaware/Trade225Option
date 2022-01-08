# -*- coding: utf-8 -*-
import datetime

def str2int( s):
    s = s.strip()
    s = removeCurls(s)
    s = s.replace(',', '')
    if s == '-':
        value = None
    else:
        try:
            value = int(s)
        except ValueError:
            value = None
    return value
    
def isFloatString(s):
    s = s.strip()
    s = s.replace('%', '')
    s = s.replace(',', '')
    s = removeCurls(s)
    try:
        value = float(s)
    except ValueError:
        return False    
    return True
        
        
def str2float( s):
    s = s.strip()
    s = s.replace('%', '')
    s = s.replace(',', '')
    s = removeCurls(s)
    if s == '-':
        value = None
    else:
        try:
            value = float(s)
        except ValueError:
            value = None
    return value

def str2floatArray( s):
    out = []
    s = s.strip()
    s = removeDoubleQuotations(s)
    values = s.split(' ')
    for value in values:
        out.append(str2float(value))
    return out

def str2intArray( s):
    out = []
    s = removeDoubleQuotations(s)
    values = s.split(' ')
    for value in values:
        out.append(str2int(value))
    return out

def str2strArray( s):
    out = []
    s = removeDoubleQuotations(s)
    values = s.split(' ')
    for value in values:
        out.append(removeCurls(value))
    return out

def removeCurls( s):
    s = s.replace('(', '')
    out = s.replace(')', '')
    return out

def removeDoubleQuotations( s):
    out = s.replace('"', '')
    return out


def today():
    return datetime.datetime.today()


def yesterday():
    return today() - datetime.timedelta(days=1)


def time2datetime(timeStr):
    values = timeStr.split(':')
    if len(values) >= 2:
        hour = int(values[0])
        minutes = int(values[1])
    else:
        return None
    now = datetime.datetime.now()
    if now.hour >= 0 and now.hour <= 6:
        if hour <= 23 and hour >= 7:
            return datetime.datetime(yesterday().year, yesterday().month, yesterday().day, hour, minutes)
    return datetime.datetime(today().year, today().month, today().day, hour, minutes)


def float2StrDQ(value):
    s = '"' + str(value) + '"'
    return s


def addDQ(s):
    s = '"' + s + '"'
    return s


def datetimeStr(time):
    return "'" + time.strftime('%Y/%m/%d %H:%M:%S') + "'"


def when(table, item, beginTime, endTime):
    sql = 'where '
    sql += table + '.' + item + ' >= ' + datetimeStr(beginTime)
    sql += ' and ' + table + '.' + item + ' <= ' + datetimeStr(endTime)
    return sql





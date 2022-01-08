# -*- coding: utf-8 -*-
from HtmlParser import HtmlParser
import toolKit
from OptionPrice import importFromTable

class OptionParser(HtmlParser):
    
    def __init__(self, html):
        super().__init__(html)
        return
    
    def parse(self, contract_month):
        nikkei225, allPrices = self.parseTable()
        return importFromTable(contract_month, allPrices)
        
    def parseTable(self):
        tables = self.soup.findAll('table',{'blue'})
        if len(tables) < 2:
            return []
        
        table = tables[0]
        tbody = table.find('tbody')
        td = tbody.find('td',{'txa_r'})
        values = self.td2Strings(td)
        nikkei225 = toolKit.str2float(values[0])
        
        table = tables[1]
        tbody = table.find('tbody')
        
        priceList = []
        for i in range(2):
            if i == 0:
                className = 'odd'
            else:
                className = 'even'
                
            trs = tbody.findAll('tr',{className})
            prices = []
            for tr in trs:
                tds = tr.findAll('td',{'txa_r'})
                colValues = []
                for i in range(len(tds)):
                    td = tds[i]
                    values = self.td2Strings(td)
                    for value in values:
                        colValues.append(value)
                prices.append(colValues)
            priceList.append(prices)
            
        size1 = len(priceList[0])   # odd
        size2 = len(priceList[1])   # even
        allPrices = []
        for i in range(size2):
            allPrices.append(priceList[0][i])
            allPrices.append(priceList[1][i])
        if size1 > size2:
            allPrices.append(priceList[0][size1 - 1])
        return (nikkei225, allPrices)
        
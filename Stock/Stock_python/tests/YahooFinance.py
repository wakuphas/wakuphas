#!/usr/local/bin/python
# -*- coding:utf-8 -*-
import jsm
import datetime
import time
import csv
import pandas as pd

#--------------------------------------------------
# 全ETF銘柄の株価データをYahooファイナンスから取得
#   →　CSVファイルに変換
# 
# Copyright 2015 Yoshihito Aso
#--------------------------------------------------


def price_to_csvl(ccode,price):
    # PriceデータをCSV出力用フォーマットに変換
    return [ccode, price.date.strftime('%Y-%m-%d'),
            price.open, price.high, price.low,
            price.close, price.volume, price._adj_close]

if __name__ == "__main__":
    
    out_file = "ETF_Stock_Prices_Daily_20050901-20151001.csv"
    c = csv.writer(open(out_file,'a'))
    c.writerow(["stock_code","date","open","high","low","close","volume","adj_close"])
    
    #データ取得期間(最大) : 上場以降のデータしか存在しないので注意
    start_date = datetime.date(2017,9,1)
    end_date = datetime.date(2017,10,1)
    print "fu"
    df = pd.read_csv('ETF_list.csv')
    stock_list = df['stock_code']
    
    for stock_code in stock_list:
        #time.sleep(10.0) #サイトに負荷をかけ過ぎないように 10sec SLEEP
        print stock_code

        try:
            q = jsm.Quotes()
            historical_prices = q.get_historical_prices(stock_code, jsm.DAILY, 
                    start_date = start_date, end_date = end_date)
            
            for price in historical_prices:
                c.writerow(price_to_csvl(stock_code, price))
        
        except(jsm.exceptions.CCODENotFoundException): #銘柄が存在しない場合は何もせずに処理継続
            print "fff"
            pass

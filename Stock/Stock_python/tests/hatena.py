#-*- coding:utf-8 -*-

# JapanStockScraping.py
# Reference:
# https://algorithm.joho.info/programming/python/jsm-get-japan-stock/

import jsm
import datetime


# get_stock(STOCK_CODE, START_DATE(yyyy-m-d), END_DATE(yyyy-m-d))
# Return: Stockprice data from START_DATE to END_DATE
#         with STOCK_CODE
#         "date, open, high, low, close, volume"
def get_stock(GET_STOCK_CODE, GET_START_DATE, GET_END_DATE):
    # Time Span
    S_YEAR, S_MONTH, S_DAY = GET_START_DATE.split("-")
    TARGET_START = datetime.date(int(S_YEAR), \
                                int(S_MONTH), \
                                int(S_DAY))
    E_YEAR, E_MONTH, E_DAY = GET_END_DATE.split("-")
    TARGET_END = datetime.date(int(E_YEAR), \
                                int(E_MONTH), \
                                int(E_DAY))

    # Get Stock Price
    Q = jsm.Quotes()
    TARGET = Q.get_historical_prices(GET_STOCK_CODE, \
                                     jsm.DAILY, \
                                     TARGET_START, \
                                     TARGET_END)

    # Return to list each quotes
    Q_DATE   = [DATA.date   for DATA in TARGET]
    Q_OPEN   = [DATA.open   for DATA in TARGET]
    Q_HIGH   = [DATA.high   for DATA in TARGET]
    Q_LOW    = [DATA.low    for DATA in TARGET]
    Q_CLOSE  = [DATA.close  for DATA in TARGET]
    Q_VOLUME = [DATA.volume for DATA in TARGET]
    return [Q_DATE, Q_OPEN, Q_HIGH, Q_LOW, Q_CLOSE, Q_VOLUME]

# print_data(STOCK_CODE, START_DATE(yyyy-m-d), END_DATE(yyyy-m-d))
# Output stockprices to CSV file.
# CSV file names "STOCK_CODE.csv".
# (ex:1111.csv)
def print_data(DATA_STOCK_CODE, DATA_START_DATE, DATA_END_DATE):
    DATA = get_stock(DATA_STOCK_CODE, \
                    DATA_START_DATE, \
                    DATA_END_DATE)

    FILENAME = str(DATA_STOCK_CODE) + ".csv"
    FILE_OUT = open(FILENAME, 'wt')

    # Print Data
    PRINT_HEADER = \
            "CODE,Date,Open,High,Low,Close,Volume"
    #print(PRINT_HEADER, file = FILE_OUT)

    for Q_DATE, Q_OPEN, Q_HIGH, Q_LOW, Q_CLOSE, Q_VOLUME \
            in list(zip(*DATA)):
        STOCK_PRICES = str(DATA_STOCK_CODE) + "," +\
                    str(Q_DATE.strftime("%y/%m/%d")) + "," +\
                    str(Q_OPEN)  + "," +\
                    str(Q_HIGH)  + "," +\
                    str(Q_LOW)   + "," +\
                    str(Q_CLOSE) + "," +\
                    str(Q_VOLUME)
        #print(STOCK_PRICES, file=FILE_OUT)

    FILE_OUT.close()

def main():
    # Open START_DATE.txt
    FILE_START = open('START_DATE.txt')
    TXT_START_DATE = FILE_START.read()
    FILE_START.close()

    # Open END_DATE.txt
    FILE_END = open('END_DATE.txt')
    TXT_END_DATE = FILE_END.read()
    FILE_END.close()

    # Open STOCK_CODE.txt
    FILE_CODE = open('STOCK_CODE.txt')
    TXT_ALL_STOCK_CODE = FILE_CODE.readlines()
    FILE_CODE.close()

    for line in TXT_ALL_STOCK_CODE:
        TXT_STOCK_CODE = line.replace('\n', '')
        print_data(TXT_STOCK_CODE, \
                    TXT_START_DATE, \
                    TXT_END_DATE)

if __name__ == "__main__":
    main()

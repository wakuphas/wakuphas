import pandas as pd
from array import array
import numpy as np


df = pd.read_csv("./code_4307.csv", header=0)
df.columns=["Date", "Open", "High", "Low", "Close", "Volume", "Trading Value"]
df["index"] = [i for i in range(len(df))]
print(df.head(10))
print "******************************"
print "code_4307.csv has been loaded!!\n\n"

stock_code = []
data = np.loadtxt("./ETF_list.txt",comments="#")
print "******************************"
print "ETF_list.txt has been loaded!!"

for i in range (0, len(data)):
    #time.sleep(10.0)
    stock_code.append(int(data[i]))

etf_list = stock_code
for etf in etf_list:
    print "etf = ", etf
    df_etf = pd.read_csv("etf_" + str(int(etf)) + ".csv", header=0)
    df_etf.columns=["Date", "Open", "High", "Low", "Close", "Volume", "Trading Value"]
    print(df_etf.head(10))

    dates = []
    closeis = []
    for d in df["Date"]:
            #try:
            date = df_etf.loc[(df_etf.Date == d), "Date"]
            #print df_etf
            #print date.values[0]
            yesterday_date = date.values[0]
            dates.append(date.values[0])
                
            close = df_etf.loc[(df_etf.Date == d), "Close"]
            if str(close.values[0]) != str("nan"):
                    yesterday_close = close.values[0]
                    closeis.append(close.values[0])
                
            else:
                    #print("nan")
                    closeis.append(yesterday_close)

    df_etf2 = pd.DataFrame({"Date_" + str(etf) : dates,
                           "Close_" + str(etf) : closeis})
        
    df = pd.concat([df, df_etf2], axis=1)
    df["diff_" + str(etf)] = (df["Close_" + str(etf)] / df["Close_" + str(etf)].shift(-1)) - 1
    print(df)
    print "end"

df.to_csv("code_4307_plus.csv")


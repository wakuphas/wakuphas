import datetime
import pandas_datareader.data as web

start = datetime.datetime(1970, 5, 16)
end   = datetime.datetime(2017, 6, 23)
nikkei225 = web.DataReader("NIKKEI225", "fred", start, end) 
%matplotlib inline
nikkei225.plot()

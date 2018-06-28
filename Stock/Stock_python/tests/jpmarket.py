import jpmarket
import datetime

start = datetime(1999, 1, 1)
end = datetime(2014, 12, 8)


stock = jpmarket.DataReader(1301, 'yahoojp', start, end)
print('stock')

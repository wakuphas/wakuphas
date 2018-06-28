import pandas as pd
from array import array
import numpy as np

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score





df = pd.read_csv("code_4307_plus.csv")
df = df.sort_values(by=["index"], ascending=False)
print(df.tail(20))


df = df.iloc[0:len(df) - 1]
print(df.tail())

df_train = df.iloc[1:len(df)-1]
df_test = df.iloc[len(df)-1:len(df)]

#print("train", df_train)
#print("test", df_test)

####
xlist = []
data = np.loadtxt("./ETF_list.txt",comments="#")
for i in range (0, len(data)):
    #time.sleep(10.0)
    xlist.append(int(data[i]))
print xlist
print "******************************"
print "ETF_list.txt has been loaded!!"
####


x_train = []
y_train = []
for s in range(0, len(df_train) - 1):
    print("x_train : ", df_train["Date"].iloc[s])
    print("y_train : ", df_train["Date"].iloc[s + 1])
    print("")
    x_train.append(df_train[xlist].iloc[s])
        
    if df_train["Close"].iloc[s + 1] > df_train["Close"].iloc[s]:
        y_train.append(1)
    else:
        y_train.append(-1)

#print(x_train)
#print(y_train)

rf = RandomForestClassifier(n_estimators=len(x_train), random_state=0)
rf.fit(x_train, y_train)


test_x = df_test[xlist].iloc[0]
test_y = rf.predict(test_x.reshape(1, -1))

print("result : ", test_y[0])

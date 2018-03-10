<<<<<<< HEAD
def myFunction():
    
    import pandas as pd
    import numpy as np
    from sklearn import linear_model
    from sklearn.metrics import mean_squared_error, r2_score
    import random as rand
    import datetime
    import sqlite3
    import csv
    
    item = 'chicken'
    
    #train steak model
    df=pd.DataFrame()
    
    time = sorted([rand.uniform(10.0,24.0) for element in range(100)])
    price = [rand.uniform(7.0,20.0) for element in range(100)]
    end_time=23.9
    df['Time']=time
    df['Time_to_close']=[end_time for row in range(len(time))]-df['Time']
    i=0
    stock=[]
    for i in range(100):
        stock.append(i)
        i+=1
    
    stock=sorted(stock,reverse=True)
    
    df.insert(0,'Current_Price',price,True)
    df.insert(0,'Target_Stock',stock,True)
    
    #df.to_csv('/home/datascience/resto/chicken.csv')
    #with open('/home/datascience/resto/chicken.csv','w') as csvfile:
    #    writer = csv.writer(csvfile, delimiter=',')
    #    writer.writerows(df)
    
    
    X=df[['Time_to_close','Current_Price']]
    
    clf=linear_model.LinearRegression().fit(df[['Time_to_close','Current_Price']],df[['Target_Stock']])
    betaPrice=clf.coef_[0,1]
    #end training
    
    price0=12.0
    amount0 = 60
    priceAndQ = [[item,price0,amount0]]
    
    conn = sqlite3.connect('resto.db')  # connection
    c = conn.cursor()
    #c.execute('DROP TABLE IF EXISTS price')
    c.execute('CREATE TABLE IF NOT EXISTS price(item TEXT, price FLOAT, quantity INTEGER)')
    #c.execute('SELECT COUNT(*) FROM price WHERE item = \'chicken\'')
    if c.fetchone()==None:
        c.executemany('INSERT INTO price VALUES(?,?,?)',priceAndQ)
    else:
        c.executemany('INSERT INTO price VALUES(?,?,?)', priceAndQ)
    conn.commit()
    conn.close()
    
    
    
    def tableFromDatabase(database, table):
        conn = sqlite3.connect(database)  # connection
        c = conn.cursor()  # get a cursor object, all SQL commands are processed by
        c.execute('SELECT * FROM %s WHERE item = \'chicken\'' % table)
        tableRows = c.fetchall()
        conn.close()
        return tableRows
    
    rows = tableFromDatabase('resto.db', 'price')
    
    currentInfo = [list(row) for row in rows]
    currentPrice=currentInfo[0][1]
    
    amountSold = 10 # increment through get_posts
    amount=amount0-amountSold
    currentHour=datetime.datetime.now().hour
    currentMinutes=datetime.datetime.now().minute
    currentTime=currentHour+currentMinutes/60.0
    
    currentData=[[currentTime,currentPrice]]
    prediction=[[float(clf.predict(currentData))]]
    
    changeInPrice=round(betaPrice*(prediction[0][0]-amount),2)
    
    newPrice = currentPrice + changeInPrice
    
    priceAndQ = [[item,newPrice,amount]]
    
    conn = sqlite3.connect('resto.db')  # connection
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS price')
    c.execute('CREATE TABLE  price(item TEXT, price FLOAT, quantity INTEGER)')
=======
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import random as rand
import datetime
import sqlite3
import csv

item = 'chicken'

#train steak model
df=pd.DataFrame()

time = sorted([rand.uniform(10.0,24.0) for element in range(100)])
price = [rand.uniform(7.0,20.0) for element in range(100)]
end_time=23.9
df['Time']=time
df['Time_to_close']=[end_time for row in range(len(time))]-df['Time']
i=0
stock=[]
for i in range(100):
    stock.append(i)
    i+=1

stock=sorted(stock,reverse=True)

df.insert(0,'Current_Price',price,True)
df.insert(0,'Target_Stock',stock,True)

df.to_csv('/home/datascience/resto/chicken.csv')
with open('/home/datascience/resto/chicken.csv','w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerows(df)


X=df[['Time_to_close','Current_Price']]

clf=linear_model.LinearRegression().fit(df[['Time_to_close','Current_Price']],df[['Target_Stock']])
betaPrice=clf.coef_[0,1]
#end training

price0=12.0
amount0 = 60
priceAndQ = [[item,price0,amount0]]

conn = sqlite3.connect('resto.db')  # connection
c = conn.cursor()
#c.execute('DROP TABLE IF EXISTS price')
c.execute('CREATE TABLE IF NOT EXISTS price(item TEXT, price FLOAT, quantity INTEGER)')
c.execute('SELECT COUNT(*) FROM price WHERE item = \'chicken\'')
if c.fetchone()==None:
    c.executemany('INSERT INTO price VALUES(?,?,?)',priceAndQ)
else:
>>>>>>> 220f230ad9fc91b3dcb9bc3eb5c5199aa0b236a9
    c.executemany('INSERT INTO price VALUES(?,?,?)', priceAndQ)
    conn.commit()
    conn.close()
    
    rows = tableFromDatabase('resto.db', 'price')
    
    print('Price of ', item,' is now ', round(rows[0][1],2))
    
    with open('somefile.txt', 'a') as the_file:
        the_file.write(''.join(['Price of ', item,' is now ', str(round(rows[0][1],2))]) + '\n')

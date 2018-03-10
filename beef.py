import datetime
import sqlite3
import pickle
import time
i=0
while i<3: #True:

    item = 'beef'

    end_time=23.0
    #end model training

    f = open('beef_clf.pickle', 'rb')
    clf = pickle.load(f)
    f.close()

    betaPrice=clf.coef_[0,1]
    #set inital values - beginning of day

    price0=32.0
    amount0 = 100
    priceAndQ = [[item,price0,amount0]]

    conn = sqlite3.connect('resto.db')  # connection
    c = conn.cursor()
    #c.execute('DROP TABLE IF EXISTS price')
    c.execute('CREATE TABLE IF NOT EXISTS price(item TEXT, price FLOAT, quantity INTEGER)')
    c.execute('SELECT COUNT(*) FROM price WHERE item = \'beef\'')
    if c.fetchone()==None:
        c.executemany('INSERT INTO price VALUES(?,?,?)',priceAndQ)
    else:
        c.executemany('INSERT INTO price VALUES(?,?,?)', priceAndQ)
    conn.commit()
    conn.close()

    #WHERE NOT EXISTS (SELECT 1 FROM price WHERE item = \'steak\''
    def tableFromDatabase(database, table):
        conn = sqlite3.connect(database)  # connection
        c = conn.cursor()  # get a cursor object, all SQL commands are processed by
        c.execute('SELECT * FROM %s WHERE item = \'beef\'' % table)
        tableRows = c.fetchall()
        conn.close()
        return tableRows

    rows = tableFromDatabase('resto.db', 'price')

    #newOrder=[{"item":"chicken","quantity":2},{"item":"veggie","quantity":1}]

    currentInfo = [list(row) for row in rows]
    currentPrice=currentInfo[0][1]
    currentAmount=currentInfo[0][2]

    #for row in newOrder:

    def tableFromDatabase(database, table):
        conn = sqlite3.connect(database)  # connection
        c = conn.cursor()  # get a cursor object, all SQL commands are processed by
        c.execute('SELECT * FROM %s WHERE item = \'beef\'' % table)
        tableRows = c.fetchall()
        conn.close()
        return tableRows

    rows = tableFromDatabase('database.db', 'orders')

    ordersInfo = [list(row) for row in rows]
    amountSold = ordersInfo[0][1]
      # increment through get_posts
    amount= currentAmount-amountSold

    currentHour=datetime.datetime.now().hour
    currentMinutes=datetime.datetime.now().minute
    currentTime=currentHour+currentMinutes/60.0
    timeToClose = end_time-currentTime

    currentData=[[timeToClose,currentPrice]]
    prediction=[[float(clf.predict(currentData))]][0][0]

    if prediction >0:
        prediction=prediction
    else:
        prediction =0


    changeInPrice=round(betaPrice*(prediction-amount),2)
    if abs(changeInPrice)>currentPrice:
        newPrice=15.0
    else:
        newPrice = currentPrice + changeInPrice

    if newPrice>55.0:
        newPrice=55.0

    if amount>0:
        amount=amount
    else:
        amount=0

    priceAndQ = [[item,newPrice,amount]]

    conn = sqlite3.connect('resto.db')  # connection
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS price')
    c.execute('CREATE TABLE  price(item TEXT, price FLOAT, quantity INTEGER)')
    c.executemany('INSERT INTO price VALUES(?,?,?)', priceAndQ)
    conn.commit()
    conn.close()

    rows = tableFromDatabase('resto.db', 'price')

    print('Price of ', item,' is now ', round(rows[0][1],2), 'prediction is ', prediction, 'amount is ', amount)

    time.sleep(.1)
    i=1

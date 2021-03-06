import datetime
import sqlite3
import pickle
import time




i=0

database_file = '/home/laetitiatam/mysite/database.db'
beef_pickle = 'beef_clf.pickle'
veggie_pickle = 'veggie_clf.pickle'
chicken_pickle = 'chicken_clf.pickle'

while i < 1: # True:

    itemBeef = 'beef'
    itemVeggie = 'veggie'
    itemChicken = 'chicken'

    end_time=23.0
    #end model training

    f = open(beef_pickle, 'rb')
    clf = pickle.load(f)
    f.close()

    betaPrice=clf.coef_[0,1]
    #set inital values - beginning of day

    price0Beef=32.0
    amount0Beef = 100
    priceAndQBeef = [[itemBeef,price0Beef,amount0Beef]]

    price0Veggie = 22
    amount0Veggie = 80
    priceAndQVeggie = [[itemVeggie, price0Veggie, amount0Veggie]]

    price0Chicken = 22
    amount0Chicken = 80
    priceAndQChicken = [[itemChicken, price0Chicken, amount0Chicken]]

    conn = sqlite3.connect(database_file)  # connection
   
    c = conn.cursor()
    #c.execute('DROP TABLE price')
    c.execute('CREATE TABLE IF NOT EXISTS price(item TEXT, dollars FLOAT, quantity INTEGER)')
    c.execute('SELECT COUNT(*) FROM price WHERE item = \'beef\'')
    if c.fetchone()[0] == 0:
        c.executemany('INSERT INTO price VALUES(?,?,?)',priceAndQBeef)
    c.execute('SELECT COUNT(*) FROM price WHERE item = \'veggie\'')
    if c.fetchone()[0] == 0:
        c.executemany('INSERT INTO price VALUES(?,?,?)', priceAndQVeggie)
        print('none')
    c.execute('SELECT COUNT(*) FROM price WHERE item = \'chicken\'')
    if c.fetchone()[0] == 0:
        c.executemany('INSERT INTO price VALUES(?,?,?)', priceAndQChicken)
        print('none')
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

    rows = tableFromDatabase('database_file', 'price')

    #newOrder=[{"item":"chicken","quantity":2},{"item":"veggie","quantity":1}]

    currentInfo = [list(row) for row in rows]
    currentPrice=currentInfo[0][1]
    currentAmount=currentInfo[0][2]

    order =[['beef', 2]]
    conn = sqlite3.connect('database_file')  # connection
    c = conn.cursor()
    #c.execute('DROP TABLE orders')
    c.execute('CREATE TABLE IF NOT EXISTS orders(item TEXT, quantity INTEGER)')
    #c.executemany('INSERT INTO orders VALUES(?,?)',order)
    conn.commit()
    conn.close()

    conn = sqlite3.connect('database_file')  # connection
    c = conn.cursor()  # get a cursor object, all SQL commands are processed by
    c.execute('SELECT COUNT(*) FROM orders WHERE item = \'beef\'')
    if c.fetchone()[0] == 0:
       amountSold=0
       print('no beef')
    else:
        c.execute('SELECT * FROM orders WHERE item = \'beef\'')
        rows = c.fetchall()
        ordersInfo = [list(row) for row in rows]
        amountSold = ordersInfo[0][1]
    conn.close()
    print('current amount is', currentAmount,'amt sold ', amountSold)
      # increment through get_posts

    amount = currentAmount-amountSold
    print('amnt ', amount)

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

    priceAndQ = [[itemBeef,newPrice,amount]]

    conn = sqlite3.connect('database_file')  # connection
    c = conn.cursor()
    #c.execute('DROP TABLE IF EXISTS price')
    #c.execute('CREATE TABLE  price(item TEXT, dollars FLOAT, quantity INTEGER)')
    c.execute('UPDATE price SET dollars = %d, quantity = %d WHERE item=\'beef\'' % (newPrice, amount))
    conn.commit()
    conn.close()

    rows = tableFromDatabase('database_file', 'price')

    print('Price of ', itemBeef,' is now ', round(rows[0][1],2), 'prediction is ', prediction, 'amount is ', amount)

    #veggie

    end_time = 23.0
    # end model training

    f = open(veggie_pickle, 'rb')
    clf = pickle.load(f)
    f.close()

    betaPrice = clf.coef_[0, 1]
    # set inital values - beginning of day

    # WHERE NOT EXISTS (SELECT 1 FROM price WHERE item = \'steak\''
    def tableFromDatabase(database, table):
        conn = sqlite3.connect(database)  # connection
        c = conn.cursor()  # get a cursor object, all SQL commands are processed by
        c.execute('SELECT * FROM %s WHERE item = \'veggie\'' % table)
        tableRows = c.fetchall()
        conn.close()
        return tableRows


    rows = tableFromDatabase('database_file', 'price')

    currentInfo = [list(row) for row in rows]
    currentPrice = currentInfo[0][1]
    currentAmount = currentInfo[0][2]

    conn = sqlite3.connect('database_file')  # connection
    c = conn.cursor()  # get a cursor object, all SQL commands are processed by
    c.execute('SELECT COUNT(*) FROM orders WHERE item = \'veggie\'')
    if c.fetchone()[0] == 0:
        amountSold = 0
    else:
        c.execute('SELECT * FROM orders WHERE item = \'veggie\'')
        rows = c.fetchall()
        ordersInfo = [list(row) for row in rows]
        amountSold = ordersInfo[0][1]
    conn.close()
    print('current amount is', currentAmount, 'amt sold ', amountSold)
    # increment through get_posts
    amount = currentAmount - amountSold

    currentHour = datetime.datetime.now().hour
    currentMinutes = datetime.datetime.now().minute
    currentTime = currentHour + currentMinutes / 60.0
    timeToClose = end_time - currentTime

    currentData = [[timeToClose, currentPrice]]
    prediction = [[float(clf.predict(currentData))]][0][0]

    if prediction > 0:
        prediction = prediction
    else:
        prediction = 0

    changeInPrice = round(betaPrice * (prediction - amount), 2)
    if abs(changeInPrice) > currentPrice:
        newPrice = 5.0
    else:
        newPrice = currentPrice + changeInPrice

    if newPrice > 30.0:
        newPrice = 30.0

    if amount > 0:
        amount = amount
    else:
        amount = 0

    priceAndQ = [[itemVeggie, newPrice, amount]]

    conn = sqlite3.connect('database_file')  # connection
    c = conn.cursor()
    #c.execute('DROP TABLE IF EXISTS price')
    #c.execute('CREATE TABLE  price(item TEXT, dollars FLOAT, quantity INTEGER)')
    c.execute('UPDATE price SET dollars = %d, quantity = %d WHERE item=\'veggie\'' % (newPrice, amount))
    conn.commit()
    conn.close()

    rows = tableFromDatabase('database_file', 'price')

    print('Price of ', itemVeggie, ' is now ', round(rows[0][1], 2), 'prediction is ', prediction, 'amount is ', amount)

    #chicken

    end_time = 23.0
    # end model training

    f = open(chicken_pickle, 'rb')
    clf = pickle.load(f)
    f.close()

    betaPrice = clf.coef_[0, 1]
    # set inital values - beginning of day

    def tableFromDatabase(database, table):
        conn = sqlite3.connect(database)  # connection
        c = conn.cursor()  # get a cursor object, all SQL commands are processed by
        c.execute('SELECT * FROM %s WHERE item=\'chicken\'' % table)
        tableRows = c.fetchall()
        conn.close()
        return tableRows


    rows = tableFromDatabase('database_file', 'price')

    currentInfo = [list(row) for row in rows]
    currentPrice = currentInfo[0][1]
    currentAmount = currentInfo[0][2]

    conn = sqlite3.connect('database_file')  # connection
    c = conn.cursor()  # get a cursor object, all SQL commands are processed by
    c.execute('SELECT COUNT(*) FROM orders WHERE item = \'chicken\'')
    if c.fetchone()[0] == 0:
        amountSold = 0
        # print('none')
    else:
        c.execute('SELECT * FROM orders WHERE item = \'chicken\'')
        rows = c.fetchall()
        ordersInfo = [list(row) for row in rows]
        amountSold = ordersInfo[0][1]
        # print('some')
    conn.close()
    print('current amount is', currentAmount, 'amt sold ', amountSold)
    # increment through get_posts
    amount = currentAmount - amountSold

    # amount+=-4
    currentHour = datetime.datetime.now().hour
    currentMinutes = datetime.datetime.now().minute
    currentTime = currentHour + currentMinutes / 60.0
    timeToClose = end_time - currentTime

    currentData = [[timeToClose, currentPrice]]
    prediction = [[float(clf.predict(currentData))]][0][0]

    if prediction > 0:
        prediction = prediction
    else:
        prediction = 0

    changeInPrice = round(betaPrice * (prediction - amount), 2)
    if abs(changeInPrice) > currentPrice:
        newPrice = 5.0
    else:
        newPrice = currentPrice + changeInPrice

    if newPrice > 30.0:
        newPrice = 30.0

    if amount > 0:
        amount = amount
    else:
        amount = 0

    priceAndQ = [[itemChicken, newPrice, amount]]

    conn = sqlite3.connect('database_file')  # connection
    c = conn.cursor()
    #c.execute('DROP TABLE IF EXISTS price')
    #c.execute('CREATE TABLE  price(item TEXT, dollars FLOAT, quantity INTEGER)')
    c.execute('UPDATE price SET dollars = %d, quantity = %d WHERE item=\'chicken\'' % (newPrice, amount))
    conn.commit()
    conn.close()

    rows = tableFromDatabase('database_file', 'price')

    print('Price of ', itemChicken, ' is now ', round(rows[0][1], 2), 'prediction is ', prediction, 'amount is ', amount)

    time.sleep(6)
    i+=1
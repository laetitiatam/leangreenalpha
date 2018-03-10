# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 17:59:53 2018

@author: lt
"""

from flask import Flask, jsonify, g, request
from sqlite3 import dbapi2 as sqlite3
import subprocess
import json 

#DATABASE = 'database.db'
#app = Flask(__name__)



DATABASE = '/home/laetitiatam/mysite/database.db'
app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None: db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def add_food(item, price, quantity):
    sql = "INSERT INTO price (item, dollars, quantity) VALUES('%s', '%f', %d)" %(item, float(price), int(quantity))
    db = get_db()
    db.execute(sql)
    res = db.commit()
    return res

def new_order(foodjson):
    food1 = foodjson[0]
    food2 = foodjson[1]
    food3 = foodjson[2]
    #foods = foodjson[0] # {"order": "5", "item": "beef"}
    # int(foods[0]['order']), foods[0]['item']
    sql = "UPDATE orders SET order_qty = ('%d') WHERE item = ('%s')" %(int(food1['order']), food1['item'])
    db = get_db()
    db.execute(sql)
    sql = "UPDATE orders SET order_qty = ('%d') WHERE item = ('%s')" %(int(food2['order']), food2['item'])
    db = get_db()
    db.execute(sql)
    sql = "UPDATE orders SET order_qty = ('%d') WHERE item = ('%s')" %(int(food3['order']), food3['item'])
    db = get_db()
    db.execute(sql)
    res = db.commit()
    return res
    
    #sql = "UPDATE orders SET order_qty = ('%d') WHERE item = ('%s')" %int(food['order']), food['item'])
    #db = get_db()
    #db.execute(sql)
    #res = db.commit()
    #return res

def find_item(name=''):
    sql = "select * from price where item = '%s' limit 1" %(name)
    db = get_db()
    rv = db.execute(sql)
    res = rv.fetchall()
    rv.close()
    return res[0]

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def find_all_items():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    result = cur.execute('SELECT * FROM price;').fetchall()
    return result


@app.route('/')
def users():
    return jsonify(hello='world')

@app.route('/add',methods=['POST'])
def add_user():
    print(add_food(item=request.form['item'], price=request.form['price'], quantity=request.form['quantity']))
    return ''

@app.route('/find_item', methods=['GET'])
def find_item_by_name():
    item_name = request.args.get('item', '')
    menu_entry = find_item(item_name)
    return jsonify(item=menu_entry['item'], price=menu_entry['price'], quantity=menu_entry['quantity'])

@app.route('/order', methods=['POST'])
def add_order():
    #print(new_order(item=request.form['item'], order=request.form['order']))
    new_order(request.get_json())
    return jsonify(request.get_json())

@app.route('/all_items', methods=['GET'])
def all_items():
    menu = find_all_items()
    return jsonify(menu)

@app.route('/chickenify')
def chickens():
    test_string = 'thsi is a test'
    with open('somefile.txt', 'a') as the_file:
        the_file.write(test_string + '\n')
    subprocess.call(['python', '/home/laetitiatam/mysite/chickened.py'])
    return 'chickens!'


@app.route('/beefify')
def run_beef():
    #subprocess.call(['python', '/home/laetitiatam/mysite/test.py'], shell=False)
    return 'Beef!'

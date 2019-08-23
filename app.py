from flask import Flask, render_template, g, request
import sqlite3
from datetime import datetime


app = Flask(__name__)



## DATABASE
def connect_db():
    sql = sqlite3.connect('/Users/anonymous/Documents/udemy/flask/4. Food Tracker App/practice_00/food_log.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite3.db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()



## ROUTES
#- INDEX
@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()


    if request.method == 'POST':
        #! Put dates in database
        date = request.form['date'] #- Assuming the date is in YYYY-MM-DD format

        dt = datetime.strptime(date, '%Y-%m-%d')
        database_date = datetime.strftime(dt, '%Y%m%d') #- We want to return this format to the db

        db.execute('insert into log_date (entry_date) values (?)', [database_date])
        db.commit()

    #! Get the dates to display
    cur = db.execute('select entry_date from log_date order by entry_date desc')
    results = cur.fetchall()

    pretty_results = []

    for i in results:
        single_date = {}
        d = datetime.strptime(str(i['entry_date']), '%Y%m%d')
        single_date['entry_date'] = datetime.strftime(d, '%B %d, %Y')

        pretty_results.append(single_date)

    return render_template('home.html', results=pretty_results)


#- VIEW
@app.route('/view/<date>')
def view(date):
    db = get_db()

    cur = db.execute('select entry_date from log_date where entry_date = ?', [date])
    result = cur.fetchone()

    d = datetime.strptime(str(result['entry_date']), '%Y%m%d')
    pretty_date = datetime.strftime(d, '%B %d, %Y')

    return render_template('day.html', date=pretty_date)


#- FOOD
@app.route('/food', methods=['GET', 'POST'])
def food():
    db = get_db()

    if request.method == 'POST':

        name = request.form['food-name']
        protein = int(request.form['protein'])
        carbohydrates = int(request.form['carbohydrates'])
        fat = int(request.form['fat'])

        calories = protein * 4 + carbohydrates * 4 + fat * 9

        
        db.execute('insert into food (name, protein, carbohydrates, fat, calories) values (?, ?, ?, ?, ?)', [name, protein, carbohydrates, fat, calories])
        db.commit()

    cur = db.execute('select name, protein, carbohydrates, fat, calories from food')
    results = cur.fetchall()

        # return '<h1>Name: {} Protein: {} Carbs: {} Fat: {}</h1>'.format(request.form['food-name'],
        #         request.form['protein'], request.form['carbohydrates'], request.form['fat'])

    return render_template('add_food.html', results=results)


if __name__ == '__main__':
    app.run()
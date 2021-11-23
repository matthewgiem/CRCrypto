from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.sql import func
from sqlalchemy.sql.functions import current_user
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class CRypto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, server_default=func.now())
    
# ## seed data
# currency = 149191
# price = 0.048
# date_created = 2021-11-2
# currency = 148167
# price = 0.049
# date_created = 2021-10-27


def __repr__(self):
    return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        price_and_coins = [request.form['add_price'], request.form['add_coins']]
        new_price_and_coins = CRypto(price=price_and_coins[0], currency=price_and_coins[1])
        try:
            db.session.add(new_price_and_coins)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue adding your values'
    else:
        data = CRypto.query.order_by(CRypto.date_created).all()
        values = []
        first = 0
        date = 0
        original_date_value = 0
        original_time_value = 0
        dont_change_percent_value = 0
        dont_change_date = 0
        break_even = 8000

        for x in data: 
            if first == 0:
                first = x.currency
                values.append([x, 0, 0, 0])
                date = x.date_created
                original_date_value = x.currency
                original_time_value = x.date_created
                dont_change_percent_value = x.currency
                dont_change_date = x.date_created

            else:
                timedelta = ((x.date_created - date).seconds + 24*60*60*(x.date_created - date).days)/(24*60*60)
                dont_change_timedelta = ((x.date_created - dont_change_date).seconds + 24*60*60*(x.date_created - dont_change_date).days)/(24*60*60)
                values.append([x, 
                ((((x.currency-first)/timedelta)*365)/first)*100, 
                ((((x.currency-dont_change_percent_value)/dont_change_timedelta)*365)/dont_change_percent_value)*100,
                (np.log(8000/(x.currency * x.price))/((((x.currency-dont_change_percent_value)/dont_change_timedelta)*365)/dont_change_percent_value))])
                date = x.date_created
                first = x.currency

        return render_template('index.html', values=values, original_value = original_date_value, original_time =original_time_value)

@app.route('/delete/<int:id>', methods=["POST","GET"])
def delete(id):
    values_to_delete = CRypto.query.get_or_404(id)

    try:
        db.session.delete(values_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'there was a problem deleting those values'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    value = CRypto.query.get_or_404(id)
    if request.method == 'POST':
        value.price = request.form['update_price']
        value.currency = request.form['update_coins']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your values'
    else:
        return render_template("update.html", value=value)

if __name__ == "__main__":
    app.run(debug=True)
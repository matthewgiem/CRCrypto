from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.sql import func
from sqlalchemy.sql.functions import current_user

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
        values = CRypto.query.order_by(CRypto.date_created).all()
        return render_template('index.html', values=values)

@app.route('/delete/<int:id>')
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
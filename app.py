from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class Reservation(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    checkin = db.Column(db.String(20), nullable=False)
    checkout = db.Column(db.String(20), nullable=False)
    room = db.Column(db.Integer, nullable=False)
    roomno = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.sno} - {self.name}"

@app.route('/')
def hello_world():  
    return render_template('index.html')

@app.route("/reserve", methods = ['GET', 'POST'])
def reserve():
    reserves = Reservation.query.all()
    if len(reserves) != 0:
        reserve = False
    else:
        reserve = True
    if (request.method == 'POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        checkin = request.form.get('checkin')
        checkout = request.form.get('checkout')
        room = request.form.get('room')
        roomno = random.randint(100, 999)
        entry = Reservation(name=name, email=email, checkin=checkin, checkout=checkout, room=room, roomno=roomno)
        db.session.add(entry)
        db.session.commit()
        print("Added to database")
    return render_template('form.html', reserve=reserve)

@app.route("/view")
def view():
    return render_template('room.html', values=Reservation.query.all())

if __name__ == '__main__':
    app.run(debug=True)
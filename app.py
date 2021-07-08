from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import urllib
import urllib.request
import json
import os

app = Flask(__name__)
app.secret_key = "Secret Key"

path = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + \
    os.path.join(path, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Crud(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    fname = db.Column(db.String(100))
    cnic = db.Column(db.String(100))
    roll = db.Column(db.String(100))
    fee = db.Column(db.String(100))

    def __init__(self, name, fname, cnic, roll, fee):
        self.name = name
        self.fname = fname
        self.cnic = cnic
        self.roll = roll
        self.fee = fee


@app.route('/', methods=['GET'])
def index():
    all_data = Crud.query.all()

    with urllib.request.urlopen("https://cms.mlcs.xyz/api/view/students_of/bsit-2016/all/") as url: 
        students = json.loads(url.read().decode())

    return render_template("index.html", all_data=all_data, students=students)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        fname = request.form['fname']
        cnic = request.form['cnic']
        roll = request.form['roll']
        fee = request.form['fee']

        my_data = Crud(name, fname, cnic, roll, fee)
        db.session.add(my_data)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update():
    if request.method == "POST":
        my_date = Crud.query.get(request.form.get('id'))
        my_date.name = request.form['name']
        my_date.fname = request.form['fname']
        my_date.cnic = request.form['cnic']
        my_date.roll = request.form['roll']
        my_date.fee = request.form['fee']

        db.session.commit()
        return redirect(url_for('index'))


@app.route('/delete/<id>/')
def delete(id):
    my_data = Crud.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)

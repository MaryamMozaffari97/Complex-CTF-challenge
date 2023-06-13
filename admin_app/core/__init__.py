from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config.from_object("core.config.Config")

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)



def get_db_connection():
    return db.session


@app.route('/')
def index():

    username = request.args.get('username')
    password = request.args.get('password')

    if not request.args:
        return render_template('login.html')
    
    conn = get_db_connection()
    query = text(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
    result = conn.execute(query).fetchone()
    if result:
        return redirect(url_for('congratulations'))
    else:
        return "Login failed."


@app.route('/congratulations')
def congratulations():
    return render_template('congratulations.html')
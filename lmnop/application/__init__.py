from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'b9a5f346-e34e-4a0b-9b2a-4e9c309c735e'

db = SQLAlchemy(app)


from application import routes
db.create_all()
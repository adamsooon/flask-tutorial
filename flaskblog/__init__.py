from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:abso2016@localhost/flask_tutorial'
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

from flaskblog import routes

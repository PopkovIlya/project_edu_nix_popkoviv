from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api


app = Flask(__name__)

api = Api(app)

user = "postgres"
password = "postgres_password"
host = "localhost:5432"
db_name = "films_one"
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from flaskr import routes


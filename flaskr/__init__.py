import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

api = Api(app)

user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
host = os.environ.get('POSTGRES_HOST')
port = os.environ.get('POSTGRES_PORT')
db_name = os.environ.get('DATABASE_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'here must be a perfect secret key'


db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)



from flaskr import routes

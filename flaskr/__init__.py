from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

api = Api(app)

user = "postgres"
password = "postgres_password"
host = "localhost:5432"
db_name = "films_site_db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hewe nust be the perfect secret key'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager(app)


from flaskr import routes

# import os
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_restx import Api
# from flask_migrate import Migrate
#
#
# app = Flask(__name__)
#
# api = Api(app)
#
# user = os.environ.get('POSTGRES_USER')
# password = os.environ.get('POSTGRES_PASSWORD')
# host = os.environ.get('POSTGRES_HOST')
# port = os.environ.get('POSTGRES_PORT')
# db_name = os.environ.get('DATABASE_NAME')
#
# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)
#
# migrate = Migrate(app, db)
#
# from flaskr import routes

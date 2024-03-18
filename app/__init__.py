from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate
import os 
# import flask migrate here

app = Flask(__name__)
app.config.from_object(Config)

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
db = SQLAlchemy(app)
# Instantiate Flask-Migrate library here
migrate = Migrate(app, db) 


from app import views

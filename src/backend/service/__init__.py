from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config.from_object(os.environ.get('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)


from service.routes import *
from service.models import Bin, Doctors

migrate = Migrate(app, db)
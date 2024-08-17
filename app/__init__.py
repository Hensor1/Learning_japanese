from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from .routes import main_blueprint
from .auth import auth_blueprint

mongo = PyMongo()
bcrypt = Bcrypt()

def create_app():
    application = Flask(__name__)
    
    application.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
    application.secret_key = 'your_secret_key'

    mongo.init_app(application)
    bcrypt.init_app(application)

    # Registrer blueprints
    application.register_blueprint(main_blueprint)
    application.register_blueprint(auth_blueprint, url_prefix='/auth')

    return application


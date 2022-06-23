from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.secret_key = 'FDsjaory8ifdshafdsahfdsa9f8wefeayewaj'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .quiz import main as quiz_app
    app.register_blueprint(quiz_app)
    return app

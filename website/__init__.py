from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='verysecretkey'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///flasksite.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    

    from .views import views
    from .auth import auth


    db.init_app(app)
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    from .models import User, Note
    create_db(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
   
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app

def create_db(app):
    if not path.exists('website/'+'flasksite.db'):
        db.create_all(app=app)
        print('database created')

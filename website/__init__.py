from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy()
db_name = "database.db"

def createApp():
    # create and configure the app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'qwerty'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    db.init_app(app)
    
    migrate = Migrate(app, db)  # initialize flask-migrate here

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Task, Project  # ensure all models are imported
    
    createDatabase(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
    
def createDatabase(app):
    # create the database if it doesn't exist
    if not path.exists(f'website/{db_name}'):
        with app.app_context():
            db.create_all()
        print(
        "------------------------------------\ndatabase initialized and created \n------------------------------------\n2024. made with ♥ by yash batish\n"
    )
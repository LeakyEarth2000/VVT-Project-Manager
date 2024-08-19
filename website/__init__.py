from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__)
db = SQLAlchemy()
DB_NAME = "database.db"

def createApp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'QWERTY'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    migrate = Migrate(app, db)  # Initialize Flask-Migrate here

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Task, Project  # Ensure all models are imported
    
    createDatabase(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
    
def createDatabase(app):
    if not path.exists(f'website/{DB_NAME}'):
        with app.app_context():
            db.create_all()
        print(
        "------------------------------------\nDatabase initialized and created \n------------------------------------\n2024. Made with ♥ by Yash Batish\n"
    )
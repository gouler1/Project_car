from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from models import User  # Импорт модели для login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from routes import *  # Импорт роутов

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создаёт таблицы при первом запуске
    app.run(debug=True)

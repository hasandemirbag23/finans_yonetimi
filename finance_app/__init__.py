from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Flask uygulaması oluştur
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'geçici-gizli-anahtar')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veritabanı oluştur
db = SQLAlchemy(app)

# Login manager ayarları
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Lütfen bu sayfaya erişmek için giriş yapın!'
login_manager.login_message_category = 'info'

# Flask 2.0+ ve SQLAlchemy 1.4+ uyumluluk için uygulama bağlamı oluştur
app.app_context().push()

from finance_app.models.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rotaları içe aktar
from finance_app import routes 
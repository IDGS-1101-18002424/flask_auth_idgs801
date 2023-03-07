import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

#Creamos una nueva instancia de SQLAlchemy
db = SQLAlchemy()

#Inicio de la app
def create_app():
    #Creamos una nueva instancia de Flask
    app = Flask(__name__)

    #Configuraciones necesarias
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Generamos una clave aleatoria de sesión de Flask
    app.config['SECRET_KEY'] = os.urandom(24)
    #Definimos la ruta a la BD
    app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:#180105!@localhost/pylogin'

    db.init_app(app)
    @app.before_first_request
    def create_all():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    #Registramos el blueprint para las rutas auth de la app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    #Registramos el blueprint para las partes no auth de la app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
    
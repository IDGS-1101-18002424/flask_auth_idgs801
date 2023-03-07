from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User


from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # Consultamos si existe un usuario ya registrado con el email
    user = User.query.filter_by(email=email).first()

    # Verificamos si el usuario existe
    # Tomamos el password y lo encriptamos
    if not user or not check_password_hash(user.password, password):
        flash('El usuario y/o contraseña son incorrectos')
        return redirect(url_for('auth.login'))  # Retornamos al Login

    # Si llegamos aqui, los datos son correctos
    # Creamos una sesión y logueamos a usuario
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['GET'])
def signup():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # Consultamos si existe un usuario ya registrado
    user = User.query.filter_by(email=email)

    if user:
        flash('el correo ya esta en uso')
        return redirect(url_for('auth.signup'))

    # Creamos un nuevo usuario
    new_user = User(email=email, name=name,
                    password=generate_password_hash(password, method='sha256'))
    # Añadimos el nuevo usuario a la BD
    db.session.add(new_user)
    db.session.commit
    return redirect(url_for('auth.signup'))


@auth.route('/logout')
def logout():
    return 'Logout'

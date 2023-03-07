from flask import Blueprint, render_template
from flask_login import login_required,current_user
from . import db 

main = Blueprint('main', __name__)

#Definimos la ruta principal
@main.route('/')
def index():
    return render_template('index.html')

#Definimos la ruta del perfil
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

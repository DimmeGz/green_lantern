from flask import Blueprint, render_template
from grocery_store.database import db
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
def profile():
    return render_template('profile.html', user=current_user.name, email=current_user.email)

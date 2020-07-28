from flask import Blueprint, render_template
from grocery_store.database import db
from flask_login import current_user, login_required

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user.name, email=current_user.email, shop=current_user.manage_stores)


@main.route('/profile/orders')
def user_orders():
    return render_template('userorders.html', user=current_user.name, orders=current_user.orders)

from flask import Blueprint
from flask_restful import Api

from grocery_store.routes.users import Users
from grocery_store.routes.goods import Goods

users = Blueprint("users", __name__)
goods = Blueprint('goods', __name__)
api_users = Api(users)
api_goods = Api(goods)

api_users.add_resource(Users, "/users", "/users/<user_id>")
api_goods.add_resource(Goods, "/goods", "/goods/<good_id>")

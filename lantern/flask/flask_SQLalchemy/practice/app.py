from config import Config
from flask import Flask
import logging

from models import User, Store, Good, db
from populate_data import get_users, get_stores, get_goods
from sqlalchemy_utils import create_database, database_exists

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
logging.basicConfig(filename="logfile.log", level=logging.INFO)

with app.app_context():
    if database_exists(db.engine.url):
        db.create_all()
        logging.info('Database exists')
    else:
        logging.info('Database does not exists')
        create_database(db.engine.url)
        logging.info('Data base created')

with app.app_context():
    users = get_users()
    for user in users:
        db.session.add(User(**user))
    db.session.commit()
    logging.info('Data written in data_base succesfuly')

with app.app_context():
    stores = get_stores()
    for store in stores:
        db.session.add(Store(**store))
    db.session.commit()
    logging.info('Data written in data_base succesfuly')

with app.app_context():
    goods = get_goods()
    for good in goods:
        db.session.add(Good(**good))
    db.session.commit()
    logging.info('Data written in data_base succesfuly')

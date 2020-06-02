from flask import Flask
import logging
from sqlalchemy_utils import create_database, database_exists

from config import Config
from models import User, Store, Good, db
from populate_data import get_users, get_stores, get_goods

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
logging.basicConfig(format='%(asctime)s %(levelname)-6s %(message)s', filename="logfile.log", level=logging.INFO)

with app.app_context():
    if not database_exists(db.engine.url):
        logging.info('Database "cursor_sqlalchemy_db" does not exists')
        create_database(db.engine.url)
        logging.info('Data "cursor_sqlalchemy_db" base created')
    db.create_all()
    logging.info('Database "cursor_sqlalchemy_db" exists')

with app.app_context():
    users = get_users()
    for user in users:
        db.session.add(User(**user))
    db.session.commit()
    logging.info('Data written to table "users" in db "cursor_sqlalchemy_db" succesfuly')

with app.app_context():
    stores = get_stores()
    for store in stores:
        db.session.add(Store(**store))
    db.session.commit()
    logging.info('Data written to table "stores" in db "cursor_sqlalchemy_db" succesfuly')

with app.app_context():
    goods = get_goods()
    for good in goods:
        db.session.add(Good(**good))
    db.session.commit()
    logging.info('Data written to table "goods" in db "cursor_sqlalchemy_db" succesfuly')

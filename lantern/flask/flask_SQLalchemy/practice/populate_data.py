import csv


def get_users():
    with open('users.csv', 'r') as u:
        reader = csv.DictReader(u)
        users = [i for i in reader]
    return users


def get_stores():
    with open('stores.csv', 'r') as s:
        reader = csv.DictReader(s)
        stores = [i for i in reader]
    return stores


def get_goods():
    with open('goods.csv', 'r') as g:
        reader = csv.DictReader(g)
        goods = [i for i in reader]
    return goods

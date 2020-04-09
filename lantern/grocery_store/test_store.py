import inject
import json
import pytest

from store_app import app
from fake_storage import FakeStorage


def configure_test(binder):
    db = FakeStorage()
    binder.bind('DB', db)


class Initializer:
    def setup(self):
        inject.clear_and_configure(configure_test)
        app.config['TESTING'] = True
        with app.test_client() as client:
            self.client = client


class TestUsers(Initializer):
    def test_create_new(self):
        resp = self.client.post(
            '/users',
            json={'name': 'John Doe'}
        )
        assert resp.status_code == 201
        assert resp.json == {'user_id': 1}
        resp = self.client.post(
            '/users',
            json={'name': 'Andrew Derkach'}
        )
        assert resp.json == {'user_id': 2}

    def test_successful_get_user(self):
        resp = self.client.post(
            '/users',
            json={'name': 'John Doe'}
        )
        user_id = resp.json['user_id']
        resp = self.client.get(f'/users/{user_id}')
        assert resp.status_code == 200
        assert resp.json == {'name': 'John Doe'}

    def test_get_unexistant_user(self):
        resp = self.client.get(f'/users/1')
        assert resp.status_code == 404
        assert resp.json == {'error': 'No such user_id 1'}

    def test_succesful_put_user(self):
        resp = self.client.post(
            '/users',
            json={'name': 'John Doe'}
        )
        user_id = resp.json['user_id']
        resp = self.client.put(
            f'/users/{user_id}',
            json={'name': 'Johanna Doe'}
        )
        assert resp.status_code == 200
        assert resp.json == {'status': 'success'}

    def test_unexistant_put_user(self):
        resp = self.client.put(
            f'/users/56',
            json={'name': 'John Doe'}
        )
        assert resp.status_code == 404


class TestGoods(Initializer):
    def test_post_goods(self):
        with open('jsons/goods.json') as goods:
            resp = self.client.post(
                '/goods',
                json=json.load(goods)
            )
        assert resp.status_code == 201
        assert resp.json == {'numbers of items created': 10}

    def test_get_goods(self):
        with open('jsons/goods.json') as goods:
            self.client.post(
                '/goods',
                json=json.load(goods)
            )
        resp = self.client.get('/goods')
        assert resp.status_code == 200
        with open('jsons/goods_updated.json') as new_goods:
            assert resp.json == json.load(new_goods)

    def test_update_goods(self):
        with open('jsons/goods.json') as goods:
            self.client.post(
                '/goods',
                json=json.load(goods)
            )
        with open('jsons/goods_for_update.json') as update:
            resp = self.client.put(
                '/goods',
                json=json.load(update)
            )
            assert resp.json == {'successfully_updated': 3,
                                 'errors': {'no such id in goods': [11, 12, 13]}}
        resp = self.client.get('/goods')
        assert resp.status_code == 200
        with open('jsons/goods_updated_2.json') as new_goods:
            assert resp.json == json.load(new_goods)


class TestStores(Initializer):
    @pytest.mark.parametrize(
        "store,answer_code,answer",
        (
                ({'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 1}, 200, {'store_id': 1}),
                ({'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 15}, 404, {'error': 'No such user_id 15'})
        )
    )
    def test_post_store(self, store, answer_code, answer):
        user = {'name': 'John Doe'}
        self.client.post('/users', json=user)
        resp = self.client.post('/stores', json=store)
        assert resp.status_code == answer_code
        assert resp.json == answer

    @pytest.mark.parametrize(
        "adress,answer_code,answer",
        (
                (1, 200, {'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 1}),
                (2, 404, {'error': 'No such store_id 2'})
        )
    )
    def test_get_store_by_id(self, adress, answer_code, answer):
        user = {'name': 'John Doe'}
        self.client.post('/users', json=user)
        newstore = {'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 1}
        self.client.post('/stores', json=newstore)
        resp = self.client.get(f'/stores/{adress}')
        assert resp.status_code == answer_code
        assert resp.json == answer

    @pytest.mark.parametrize(
        "update,adress,answer_code,answer",
        (
                ({'name': 'Local Taste', 'location': 'Lviv', 'manager_id': 1}, 1, 201, {'status': 'success'}),
                ({'name': 'Local Taste', 'location': 'Lviv', 'manager_id': 1}, 21, 404,
                 {'error': 'No such store_id 21'}),
                ({'name': 'Local Taste', 'location': 'Lviv', 'manager_id': 15}, 1, 404, {'error': 'No such user_id 15'})

        )
    )
    def test_update_store_by_id(self, update, adress, answer_code, answer):
        user = {'name': 'John Doe'}
        self.client.post('/users', json=user)
        newstore = {'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 1}
        self.client.post('/stores', json=newstore)
        resp = self.client.put(f'/stores/{adress}', json=update)
        assert resp.status_code == answer_code
        assert resp.json == answer

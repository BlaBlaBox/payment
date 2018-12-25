import requests
import pytest

# Usage pytest -q test.py

# link -> https://blablabox-transaction.herokuapp.com


class TestClass(object):
    base_url = 'https://blablabox-transaction.herokuapp.com'

    def test_create_cart(self):
        r = requests.post(url=self.base_url+'/cart/create/1')
        assert r.status_code == 200 or r.status_code == 400

    def test_create_item(self):
        l = {
            'movie_id': '1',
            'price': '123',
            'duration': '1234'
        }

        r = requests.post(url=self.base_url+'/cart/item/create/1', json=l)
        assert r.status_code == 200 or r.status_code == 400

    def test_update_item(self):
        l = {
            'movie_id': '1',
            'price': '4',
            'duration': '1234'
        }

        r = requests.post(url=self.base_url+'/cart/item/update/1', json=l)
        assert r.status_code == 200 or r.status_code == 400

    def test_get_cart(self):
        r = requests.get(url=self.base_url+'/cart/get/1')
        assert r.status_code == 200 or r.status_code == 400

    def test_pay(self):
        l = {
            'holder': 'ALPEREN KANTARCI',
            'expiration': '1219',
            'number': '5105105105105105',
            'cvc': '510',
            'cost': '1'
        }

        r = requests.post(url=self.base_url+'/payment/pay/1', json=l)
        assert r.status_code == 200 or r.status_code == 400

    def test_rent(self):
        r = requests.get(url=self.base_url+'/payment/rent/get/1')
        assert r.status_code == 200 or r.status_code == 400

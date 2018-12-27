import string
import random
import requests
import pytest

from random import randint
# Usage: pytest -q test.py


class PaymentAction():
    base_url = 'https://blablabox-transaction.herokuapp.com'

    # For local testing
    # base_url = 'http://127.0.0.1:8000'

    def create_cart(self, user_id, required_status):
        r = requests.post(url=self.base_url + '/cart/create/' + user_id)
        assert r.status_code == required_status

    def create_item(self, user_id, item_dict, required_status):
        r = requests.post(url=self.base_url + '/cart/item/create/' + user_id, json=item_dict)
        assert r.status_code in required_status

    def delete_item(self, user_id, movie_id_dict, required_status):
        r = requests.post(url=self.base_url + '/cart/item/delete/' + user_id, json=movie_id_dict)
        assert r.status_code == required_status

    def update_item(self, user_id, item_dict, required_status):
        r = requests.post(url=self.base_url + '/cart/item/update/' + user_id, json=item_dict)
        assert r.status_code == required_status

    def get_cart(self, user_id, required_status):
        r = requests.get(url=self.base_url + '/cart/get/' + user_id)
        assert r.status_code == required_status

    def pay(self, user_id, credit_card_info, required_status):
        r = requests.post(url=self.base_url + '/payment/pay/' + user_id, json=credit_card_info)
        assert r.status_code == required_status

    def get_rent(self, user_id, required_status):
        r = requests.get(url=self.base_url + '/payment/rent/get/' + user_id)
        assert r.status_code == required_status

    def send_end_test(self, status):
        resp = requests.get(self.base_url + "/endtest")
        assert resp.status_code == status


def test_payment_actions():
    pAction = PaymentAction()

    # Valid card item
    cart_item = {
        'movie_id': '1',
        'price': '123',
        'duration': '1234'
    }

    # Valid card holder
    valid_credit_card = {
        'holder': 'ECEM GULDOSUREN',
        'expiration': '1123',
        'number': '1234567890123456',
        'cvc': '112',
        'cost': '1'
    }

    # Valid and invalid user
    valid_user, invalid_user = str(1), str(100000000000)

    # Create card with user that has a cart
    pAction.create_cart(valid_user, 400)

    # Create card with user that is not valid
    pAction.create_cart(invalid_user, 500)

    # Create item for valid user might have already or not
    pAction.create_item(valid_user, cart_item, [200, 400])

    # Update item in the basket
    new_cart_item = cart_item.copy()
    new_cart_item['price'] = str(randint(0, 100))
    pAction.update_item(valid_user, new_cart_item, 200)

    # Update item that has big price
    new_cart_item = cart_item.copy()
    new_cart_item['price'] = str(randint(10000, 1000000))
    pAction.update_item(valid_user, new_cart_item, 500)

    # Get cart of valid user
    pAction.get_cart(valid_user, 200)

    # Get cart of invalid user
    pAction.get_cart(invalid_user, 500)

    # Pay with valid credit card
    pAction.pay(valid_user, valid_credit_card, 200)

    # Pay with invalid user
    pAction.pay(invalid_user, valid_credit_card, 500)

    # Pay with invalid credit card
    invalid_cd = valid_credit_card.copy()
    invalid_cd['holder'] = 'Test'
    pAction.pay(valid_user, invalid_cd, 402)

    # Pay with invalid credit card and invalid user
    pAction.pay(invalid_user, invalid_cd, 402)

    # Pay with invalid json structure
    pAction.pay(invalid_user, {'cvc': 5}, 402)

    # Try get rent with valid user
    pAction.get_rent(valid_user, 200)

   # Try get rent with unvalid user
    pAction.get_rent(invalid_user, 400)

    # Send a request to complete coverage report
    pAction.send_end_test(200)

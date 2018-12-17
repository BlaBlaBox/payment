from flask import jsonify, request, abort
import requests
from payment_config import app
from datetime import datetime
from payment_db import add_cart, complete_cart, add_item, remove_item, update_item
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def not_found(error):
    return jsonify({'error': 'Your request doesn\'t contain JSON'}), 400

@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 403


# The create action of payment
@app.route('/cart/create/<int:user_id>', methods=['POST'])
#@auth.login_required
def create_cart(user_id):
    new_cart = add_cart(user_id)
    if new_cart == None:
        return jsonify({'error': 'There is already a cart which is not finished.'}), 400
    return jsonify({'result': 'Success','cart_id':new_cart.trans_id}), 200

@app.route('/cart/item/create/<int:user_id>', methods=['POST'])
#@auth.login_required
def create_item(user_id):
    if not request.json:
        abort(400)

    movie_id = request.json['movie_id']
    price = request.json['price']
    duration = request.json['duration']

    new_item = add_item(user_id,movie_id,price,duration)
    if new_item == None:
        return jsonify({'error': 'Item is already in the cart.'}), 400
    return jsonify({'result': 'Success','item_id':new_item.trans_id}), 200


@app.route('/cart/item/delete/<int:user_id>', methods=['POST'])
#@auth.login_required
def delete_item(user_id):
    if not request.json:
        abort(400)

    movie_id = request.json['movie_id']

    new_item = remove_item(user_id,movie_id)
    return jsonify({'result': 'Success'}), 200

@app.route('/cart/item/update/<int:user_id>', methods=['POST'])
#@auth.login_required
def update_item(user_id):
    if not request.json:
        abort(400)

    movie_id = request.json['movie_id']
    price = request.json['price']
    duration = requests.json['duration']

    new_item = remove_item(user_id,movie_id)
    return jsonify({'result': 'Success','item_id':new_item.trans_id}), 200

@app.route('/cart/get/<int:user_id>', methods=['POST'])
#@auth.login_required
def get_cart(user_id):
    if not request.json:
        abort(400)



    new_item = remove_item(user_id,movie_id)
    return jsonify({'result': 'Success','item_id':new_item.trans_id}), 200


@app.route('/payment/pay/<int:user_id>', methods=['POST'])
#@auth.login_required
def pay(user_id):
    if not request.json:
        abort(400)
    
    url = 'http://127.0.0.1:7000/creditcard/pay'

    response = requests.post(url, json=request.json,headers={'Content-Type': 'application/json'})
    print(response.status_code)
    result = response.status_code
    
    if result == 200:
        cart = complete_cart(user_id)
        new_cart = add_cart(user_id)
        if new_cart == None:
            return jsonify({'error': 'There is already a cart which is not finished.'}), 400 
        return jsonify({'result': 'Success'}), 200
    else:
        return response.content


# Validate the admin signin
@auth.verify_password
def verify_password(username, password):
    # TODO: Change check if is admin in the database or not.
    return username == 'admin' and password == 'asdqwe123'


if __name__ == '__main__':
    app.run(debug=True, port=8000) 
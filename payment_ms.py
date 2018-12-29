from flask import jsonify, request, abort           # pragma: no cover
import requests                                     # pragma: no cover
from payment_config import app                      # pragma: no cover
from payment_db import add_cart, complete_cart, add_item, remove_item, update_item_db, get_cart_items, get_rented_movies  # pragma: no cover
from coverage import Coverage, CoverageException    # pragma: no cover


@app.errorhandler(400)  # pragma: no cover
def bad_request(error):
    return jsonify({'error': 'Your request doesn\'t contain JSON'}), 400


@app.errorhandler(401)  # pragma: no cover
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 403


@app.errorhandler(404)  # pragma: no cover
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


cov = Coverage()            # pragma: no cover
cov.start()                 # pragma: no cover


# The create action of payment
@app.route('/cart/create/<int:user_id>', methods=['POST'])
def create_cart(user_id):
    new_cart = add_cart(user_id)
    if new_cart is None:
        return jsonify({'error': 'There is already a cart which is not finished.'}), 400
    return jsonify({'result': 'Success', 'cart_id': new_cart.trans_id}), 200


@app.route('/cart/item/create/<int:user_id>', methods=['POST'])
def create_item(user_id):
    if not request.json:
        abort(400)  # pragma: no cover

    movie_id = request.json['movie_id']
    price = request.json['price']
    duration = request.json['duration']

    new_item = add_item(user_id, movie_id, price, duration)
    if new_item is None:
        return jsonify({'error': 'Item is already in the cart.'}), 400
    return jsonify({'result': 'Success'}), 200


@app.route('/cart/item/update/<int:user_id>', methods=['POST'])
def update_item(user_id):
    if not request.json:
        abort(400)  # pragma: no cover

    movie_id = request.json['movie_id']
    price = request.json['price']
    duration = request.json['duration']

    update_item_db(user_id, movie_id, price, duration)
    return jsonify({'result': 'Success'}), 200


@app.route('/cart/get/<int:user_id>', methods=['GET'])
def get_cart(user_id):

    items = get_cart_items(user_id)
    if items is None:
        return jsonify({'error': 'There is no item in the cart.'}), 400

    item_list = []
    for item in items:
        item_list.append({"movie_id": str(item.movie_id), "price": str(item.price), "duration": str(item.duration)})

    return jsonify({'result': 'Success', 'item_list': item_list}), 200


@app.route('/payment/pay/<int:user_id>', methods=['POST'])
def pay(user_id):
    if not request.json:
        abort(400)      # pragma: no cover

    URL = 'http://blablabox-bank.herokuapp.com/creditcard/pay'

    response = requests.post(URL, json=request.json)
    print(response.status_code)
    result = response.status_code

    if result == 200:
        cart = complete_cart(user_id)
        new_cart = add_cart(user_id)
        if new_cart is None:
            return jsonify({'error': 'There is already a cart which is not finished.'}), 400
        return jsonify({'result': 'Success'}), 200
    else:
        return jsonify({'error': 'There is problem with the bank service.'}), 402


@app.route('/payment/rent/get/<int:user_id>', methods=['GET'])
def get_rented(user_id):
    movies = get_rented_movies(user_id)
    movies_list = []
    if movies is None:
        return jsonify({'error': 'There is no movie to shown.'}), 400
    for movie in movies:
        movies_list.append({"movie_id": str(movie.movie_id)})
    return jsonify({'result': 'Success', 'movies_list': movies_list}), 200


@app.route('/endtest')  # pragma: no cover
def end_test():
    cov.stop()
    cov.save()
    try:
        cov.html_report()
        return jsonify({'result': 'Coverage report has been saved'}), 200
    except CoverageException as err:
        print("Error ", err)
        return jsonify({'result': 'Error on coverage'}), 400


if __name__ == '__main__':      # pragma: no cover
    app.run(debug=True, port=8000)

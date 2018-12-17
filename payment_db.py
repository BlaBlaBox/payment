from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from payment_config import app

db = SQLAlchemy(app)
#db.drop_all()

class carttrans(db.Model):
    trans_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,nullable=False)
    trans_time = db.Column(db.DateTime, default=(datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
    is_completed = db.Column(db.Boolean, default=False)



class itemtrans(db.Model):
    trans_id = db.Column(db.Integer,db.ForeignKey('carttrans.trans_id'),primary_key=True)
    movie_id = db.Column(db.Integer,primary_key=True)
    price = db.Column(db.Numeric(precision=5,scale=2))
    duration = db.Column(db.Integer,default=-1)



def add_db(obj):
    try:
        db.session.add(obj)
        db.session.commit()
        return obj
    except:
        db.session.rollback()
        raise

def remove_db(obj):
    try:
        db.session.delete(obj)
        db.session.commit()
    except:
        db.session.rollback()
        raise

def commit_db():
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise

# Not completed carts should be detected afterwards
def add_cart(user_id):
    cart_obj = carttrans.query.filter_by(user_id=user_id).filter_by(is_completed=False).first()
    if cart_obj:
        return None

    new_cart = carttrans(user_id=user_id)
    return add_db(new_cart)

def complete_cart(user_id):
    cart_obj = carttrans.query.filter_by(user_id=user_id).filter_by(is_completed=False).first()
    cart_obj.is_completed = True 
    commit_db()
    return cart_obj

def add_item(user_id,movie_id,price,duration):
    cart_obj = carttrans.query.filter_by(user_id=user_id).filter_by(is_completed=False).first()
    search_item = itemtrans.query.filter_by(movie_id=movie_id).filter_by(trans_id=cart_obj.trans_id).first()
    if search_item:
        return None 
    new_item = itemtrans(trans_id=cart_obj.trans_id,movie_id=movie_id,price=price,duration=duration)
    return add_db(new_item)
    
def remove_item(user_id,movie_id):
    cart_obj = carttrans.query.filter_by(user_id=user_id).filter_by(is_completed=False).first()
    item = itemtrans.query.filter_by(trans_id=cart_obj.trans_id,movie_id=movie_id).first()
    remove_db(item)
    return True

## BURADA HATA OLABILIR FRONTENDDE BAKILMASI LAZIM
def update_item(user_id,movie_id,price,duration):
    try:
        cart_obj = carttrans.query.filter_by(user_id=user_id).filter_by(is_completed=False).first()
        rent_obj = carttrans.query.filter_by(trans_id=cart_obj.trans_id).filter_by(movie_id=rent_id).first()
        rent_obj.price = price
        rent_obj.duration = duration 
        db.session.commit()
        return rent_obj
    except:
        db.session.rollback()
        raise


def get_cart_items(user_id):
    cart_obj = carttrans.query.filter_by(user_id=user_id).filter_by(is_completed=False).first()
    items = itemtrans.query.filter_by(trans_id=cart_obj.trans_id).all()
    return items    

def get_rented_movies(user_id):
    carts = carttrans.query.filter_by(user_id=user_id).filter_by(is_completed=True).all()
    rented_movies = []
    for cart in carts:
        movies = itemtrans.query.filter_by(trans_id=cart.trans_id).filter(itemtrans.duration!=0).all()
        for i in movies:
            rented_movies.append(i)
    return rented_movies if rented_movies != [] else None   

db.create_all()
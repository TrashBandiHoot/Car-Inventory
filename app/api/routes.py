
from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'foo': 'bar'}

# !COPIED FROM PHONEBOOK APP -- MUST CHANGE, THIS IS FOR REFERENCE ONLY

@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    year = request.json['year']
    brand = request.json['brand']
    model = request.json['model']
    price = request.json['price']
    zero_to_sixty = request.json['zero_to_sixty']
    top_speed = request.json['top_speed']
    gas = request.json['gas']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(year, brand, model, price, zero_to_sixty, top_speed, gas, user_token = user_token )

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)



@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)



# Updating
@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    car.year = request.json['year']
    car.brand = request.json['brand']
    car.model = request.json['model']
    car.price = request.json['price']
    car.zero_to_sixty = request.json['zero_to_sixty']
    car.top_speed = request.json['top_speed']
    car.gas = request.json['gas']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# Delete
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)
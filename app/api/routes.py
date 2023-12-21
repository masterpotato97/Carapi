from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, CarSchema, car_schema, car_schemas

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'my':'data'}

@api.route('/car', methods = ['POST'])
@token_required
def create_car(current_user_token):
    print(request.json)
    name = request.json['name']
    make=request.json['make']
    model = request.json['carmodel']
    address = request.json['address'] 
    
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(name, model, make, address, user_token = user_token )

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token = a_user).all()
    print(cars)
    response = car_schemas.dump(cars)
    return jsonify(response)




@api.route('/cars/<id>', methods=['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id) 
    car.name = request.json['name']
    car.make = request.json['make']
    car.model = request.json['model']
    car.address = request.json['address'] 
    
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)



@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)
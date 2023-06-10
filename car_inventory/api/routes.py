from flask import Blueprint, request, jsonify
from car_inventory.helpers import token_required
from car_inventory.models import db,User,Car,car_schema,cars_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/cars', methods=['POST'])
@token_required
def create_car(current_user_token):
    make_model=request.json['make_model']
    description=request.json['description']
    price=request.json['price']
    max_speed=request.json['max_speed']
    fuel_type=request.json['fuel_type']
    title=request.json['title']
    accidents=request.json['accidents']
    mileage=request.json['mileage']
    location=request.json['location']
    user_token=current_user_token.token

    print(f'BIG TESTER {current_user_token}')

    car=Car(make_model,description,price,max_speed,fuel_type,title,accidents,mileage,location,user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response=car_schema.dump(car)
    return jsonify(response)


@api.route('/cars',methods=["GET"])
@token_required
def get_cars(current_user_token):
    cars=Car.query.filter_by(user_token=current_user_token.token).all()
    response=cars_schema.dump(cars)
    return jsonify(response)

@api.route('/cars/<id>',methods=["GET"])
@token_required
def get_single_car(current_user_token,id):
    car=Car.query.get(id)
    response=car_schema.dump(car)
    return jsonify(response)


@api.route('/cars/<id>', methods=['POST','PUT'])
@token_required
def update_car(current_user_token,id):
    car=Car.query.get(id)
    car.make_model=request.json['make_model']
    car.description=request.json['description']
    car.price=request.json['price']
    car.max_speed=request.json['max_speed']
    car.fuel_type=request.json['fuel_type']
    car.title=request.json['title']
    car.accidents=request.json['accidents']
    car.mileage=request.json['mileage']
    car.location=request.json['location']
    car.user_token=current_user_token.token

    db.session.commit()

    response=car_schema.dump(car)
    return jsonify(response)


@api.route('/cars/<id>', methods=['DELETE'])
@token_required
def delete_car(current_user_token,id):
    car=Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response=car_schema.dump(car)
    return jsonify(response)
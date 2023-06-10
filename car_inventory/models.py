from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

from flask_login import UserMixin,LoginManager
from flask_marshmallow import Marshmallow

db =SQLAlchemy()

login_manager=LoginManager()
ma=Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id=db.Column(db.String,primary_key=True)
    first_name=db.Column(db.String(150),nullable=True,default='')
    last_name=db.Column(db.String(150),nullable=True,default='')
    email=db.Column(db.String(150),nullable=False)
    password=db.Column(db.String,nullable=True,default='')
    g_auth_verify=db.Column(db.Boolean,default=False)
    token=db.Column(db.String, default='', unique=True)
    date_created=db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    def __init__(self, email, first_name='', last_name='', id='', password='', token='', g_auth_verify=False):
        self.id=self.set_id()
        self.first_name=first_name
        self.last_name=last_name
        self.password=self.set_password(password)
        self.email=email
        self.token=self.set_token(24)
        self.g_auth_verify=g_auth_verify

    def set_token(self,length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self,password):
        self.pw_hash=generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f'User {self.email} was added to the database'
    

class Car(db.Model):
    id=db.Column(db.String,primary_key=True)
    make_model=db.Column(db.String(150))
    description=db.Column(db.String(200), nullable=True)
    price=db.Column(db.Numeric(precision=10,scale=2))
    max_speed=db.Column(db.String(100))
    fuel_type=db.Column(db.String(150))
    title=db.Column(db.String(150))
    accidents=db.Column(db.Numeric(precision=5,scale=0))
    mileage=db.Column(db.Numeric(precision=8,scale=0))
    location=db.Column(db.String(150))
    user_token=db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self,make_model,description,price,max_speed,fuel_type,title,accidents,mileage,location,user_token,id=''):
        self.id=self.set_id()
        self.make_model=make_model
        self.description=description
        self.price=price
        self.max_speed=max_speed
        self.fuel_type=fuel_type
        self.title=title
        self.accidents=accidents
        self.mileage=mileage
        self.location=location
        self.user_token=user_token


    def __repr__(self):
        return f'The following car was added: {self.make_model}'
    
    def set_id(self):
        return (secrets.token_urlsafe())

class CarSchema(ma.Schema):
    class Meta:
        fields=['id','make_model','description','price','max_speed','fuel_type','title','accidents','mileage','location']

car_schema=CarSchema()
cars_schema=CarSchema(many=True)
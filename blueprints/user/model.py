from blueprints import db
from flask_restful import fields

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    brewCount = db.Column(db.Integer, nullable=False, default=0)
    recipeCount = db.Column(db.Integer, nullable=False, default=0)
    photo = db.Column(db.String(250), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    role = db.Column(db.Integer, nullable=False)

    responseFieldsDetails = {
        'id': fields.Integer,
        'email': fields.String,
        'password': fields.String,
        'name': fields.String,
        'brewCount' : fields.Integer,
        'recipeCount' : fields.Integer,
        'photo' : fields.String,
        'status': fields.Integer,
        'role' : fields.Integer
    }

    responseFieldsJwt = {
        'id': fields.Integer,
        'email': fields.String,
        'name': fields.String,
        'brewCount' : fields.Integer,
        'recipeCount' : fields.Integer,
        'photo' : fields.String,
        'status': fields.Integer,
        'role' : fields.Integer
    }

    def __init__(self, email, password, name, brewCount, recipeCount, photo, status, role):
        self.email = email
        self.password = password
        self.name = name
        self.brewCount = brewCount
        self.recipeCount = recipeCount
        self.photo = photo
        self.status = 1
        self.role = 0

    
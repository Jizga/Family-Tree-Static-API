"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Person
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/member', methods=['POST'])
def add_member():
    body_request = request.get_json()
    
    name = body_request.get("name", None)
    last_name = body_request.get("lastName", None)
    age = body_request.get("age", None)
    parent_one_id = body_request.get("parentOneId", None)
    parent_two_id = body_request.get("parentTwoId", None)
    
    member = Person(
        name = name,
        last_name = last_name,
        age = age,
        parent_one_id = parent_one_id,
        parent_two_id = parent_two_id
    )
    
    db.session.add(member)
    db.session.commit()
    
    return jsonify(member.serialize()), 201

@app.route('/all', methods=['GET'])
def get_all_family_members():
    
    family = []
    response_family = Person.query.all()
    
    for member in response_family:
        family.append(member.serialize())
    
    return jsonify(family), 200
    
    
    
    
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

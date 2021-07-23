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
from models import db, Person, Relations
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


@app.route('/member', methods=['POST'])
def add_member():
    body_request = request.get_json()
    
    name = body_request.get("name", None)
    last_name = body_request.get("lastName", None)
    age = body_request.get("age", None)
    relations = body_request.get("relations", None)
    
    member = Person(
        name = name,
        last_name = last_name,
        age = age,
        relations = relations
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

@app.route('/member/<int:id>', methods=['GET'])
def get_single_member(id):
    
    body = request.get_json()
    member_selected = Person.query.get(id)
    
    return jsonify(member_selected.serialize()), 200
    
    
    
    
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

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

@app.route('/person', methods=['POST'])
def add_member():
    body_request = request.get_json()
    
    name = body_request.get("name", None)
    last_name = body_request.get("lastName", None)
    age = body_request.get("age", None)
    
    member = Person(
        name = name,
        last_name = last_name,
        age = age
    )
    
    db.session.add(member)
    db.session.commit()
    
    return jsonify(member.serialize()), 201

@app.route('/relation', methods=['POST'])
def add_relation():
    body_request = request.get_json()
    
    person_id = body_request.get("person_id", None)
    family_member_id = body_request.get("family_member_id", None)
    relation_type = body_request.get("relation_type", None)
    
    relation = Relations(
        person_id = person_id,
        family_member_id = family_member_id,
        relation_type = relation_type
    )
    
    db.session.add(relation)
    db.session.commit()
    
    return jsonify(relation.serialize()), 201

@app.route('/all', methods=['GET'])
def get_all_family_members():
    
    family = []
    response_family = Person.query.all()
    
    for member in response_family:
        family.append(member.serialize())
    
    # Ordernar la familia de mayor a menor
    family.sort(key=lambda member: member['age'], reverse=True)
        
    return jsonify(family), 200

@app.route('/relations', methods=['GET'])
def get_all_relations_types():
    
    relations = []
    response_relations = Relations.query.all()
    
    for relation in response_relations:
        relations.append(relation.serialize())
    
    return jsonify(relations), 200

@app.route('/person/<int:id>', methods=['GET'])
def get_single_member(id):
    
    body = request.get_json()
    person_selected = Person.query.get(id)
    # --- Para hacer las uniones entre familiares y que salgan en Postman ---
    relations_person = person_selected.relations
    
    person = person_selected.serialize()
    relations = []
    
    for relation in relations_person:
        # ----- Para hacer las uniones entre familiares y que salgan en Postman ----
        family_member = relation.family_member.serialize()
        relation_res = relation.serialize()
        
        # Añadir al Objeto "relation_res" la propiedad "person"
        relation_res['person'] = family_member
        relations.append(relation_res)
    
    # Añadir al Objeto "person" la propiedad "relations"  
    person['relations'] = relations
    
    return jsonify(person), 200

@app.route('/relation/<int:id>', methods=['GET'])
def get_single_relation(id):
    
    body = request.get_json()
    relation_selected = Relations.query.get(id)
    person_selected = relation_selected.person
    
    relation = relation_selected.serialize()
    person = person_selected.serialize()
    
    relation['person'] = person
    
    return jsonify(relation), 200
    
       
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

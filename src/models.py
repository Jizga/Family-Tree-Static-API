from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()
        
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    
    relations = db.relationship('Relations',  backref = 'person', lazy = 'dynamic', foreign_keys ='Relations.person_id')
    family_member = db.relationship('Relations',  backref = 'family_member', lazy = 'dynamic', foreign_keys ='Relations.family_member_id')
    
    
    def __repr__(self):
        return '<Person %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "age": self.age,
            "relations": list(map(lambda x: x.serialize(), self.relations))
        }
        
class Relations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    family_member_id = db.Column(db.Integer, db.ForeignKey("person.id")) 
    relation_name = db.Column(db.String(120), nullable=True)
    
    
    def __repr__(self):
        return '<Relations>'
        
    def serialize(self):
        return {
            "id": self.id,
            "person_id": self.person_id,
            "family_member_id": self.family_member_id,
            "relation_name": self.relation_name
        }
    
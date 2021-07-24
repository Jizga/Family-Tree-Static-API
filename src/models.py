from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()
        
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    
    # --- Para poder usar 2 foreign_keys que hacen referencia a una misma tabla
    # y para poder hacer la relación entre personas
    relations = db.relationship('Relations', backref = 'person', lazy='joined', foreign_keys ='Relations.person_id')
    family_member = db.relationship('Relations',  backref = 'family_member', lazy = 'joined', foreign_keys ='Relations.family_member_id')
    
    def __repr__(self):
        return '<Person %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "age": self.age
        }
        
class Relations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    family_member_id = db.Column(db.Integer, db.ForeignKey("person.id")) 
    relation_type = db.Column(db.String(120), nullable=True)
    
    def __repr__(self):
        return '<Relations>'
        
    def serialize(self):
        return {
            # Sólo interesa sacar el tipo de relación, ya que el resto de la info la aporta la tabla "Person"
            "relation_type": self.relation_type
        }
    
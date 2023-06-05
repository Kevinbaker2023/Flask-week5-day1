from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash

user_pokemon = db.Table(
    'user_pokemon',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    caught = db.relationship('Pokemon',
        secondary = user_pokemon,
        backref = db.backref('user_pokemon', lazy='dynamic),
        lazy='dynamic'
    )
    

    def hash_password(self, signup_password):
        return generate_password_hash(signup_password)
    
    def from_dict(self, user_data):
        self.first_name = user_data['first_name']
        self.last_name = user_data['last_name']
        self.email = user_data['email']
        self.password = self.hash_password(user_data['password'])

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon_name = db.Column(db.String, nullable=False)


    def from_dict(self, poke_data):
        self.pokemon_name = poke_data['pokemon_name']

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

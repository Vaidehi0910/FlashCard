
from flask_sqlalchemy.model import Model
from database import db
from flask_login import UserMixin
 
class Username(db.Model, UserMixin):
    __tablename__='username'
    user_id= db.Column(db.Integer, autoincrement=True, primary_key=True)
    username= db.Column(db.String, unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)

    def get_id(self):
        return str(self.user_id)

class Deck(db.Model):
    __tablename__='deck'
    deck_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    deck_name=db.Column(db.String, unique=True, nullable=False)
    score=db.Column(db.String, nullable=False)
    time=db.Column(db.String)
    card=db.relationship("Card", secondary="deck_card")
    # user=db.relationship("Username", secondary="user_deck")
    

class Card(db.Model):
    __tablename__='card'
    Card_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    card_front=db.Column(db.String, nullable=False)
    card_back=db.Column(db.String, nullable=False)
    score=db.Column(db.String, nullable=False)
    deck=db.relationship("Deck", secondary="deck_card")

class Deck_Card(db.Model):
    __tablename__='deck_card'
    dc_id= db.Column(db.Integer, autoincrement=True, primary_key=True)
    deck_id= db.Column(db.Integer, db.ForeignKey("deck.deck_id"), nullable=False)
    card_id=db.Column(db.Integer, db.ForeignKey("card.Card_id") , nullable=False)

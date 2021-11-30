from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api
from config import LocalDevelopmentConfig
from flask_login import LoginManager

from database import db

app=None
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
app.config['SECRET_KEY']="thisisasecretkey"
db=SQLAlchemy()
db.init_app(app)
app.config.from_object(LocalDevelopmentConfig)
app.app_context().push()
api=Api(app)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return Username.query.get(int(user_id))


from validation import *
from api import CardAPI, DeckAPI, UserAPi
api.add_resource(UserAPi,"/api/login/<string:username>/<string:password>")
api.add_resource(DeckAPI,"/api/deck", "/api/deck/<int:deck_id>")
api.add_resource(CardAPI,"/api/card/<int:deck_id>", "/api/card")

if __name__=="__main__":

    

    app.debug=True
    app.run()

    
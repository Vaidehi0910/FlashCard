from flask import Flask, request
from flask import render_template
from flask import current_app as app
from flask.helpers import url_for
from flask_login.utils import login_required, login_user, logout_user
from sqlalchemy.orm import session
from werkzeug.utils import redirect
from model import Card, Deck, Deck_Card, Username
from database import db
from flask_login import login_user
from datetime import datetime

import json

deckid=None

@app.route("/login", methods=["GET","POST"])
def login():
    error=None
    if request.method=="GET":
        return render_template("login.html",error=error)
    if request.method=="POST":
        uname=request.form["username"]
        pas=request.form["password"]
        if '"' in uname or "'" in uname:
            error="Enter a valid username"
            return render_template("sign-in.html",error=error)
        if '"' in pas or "'" in pas:
            error="Enter a valid password"
            return render_template("sign-in.html",error=error)
        user=db.session.query(Username).filter(Username.username==uname).first()
        if user is None:
            return render_template("sign-in.html")
        passw=user.password
        # if name is None:
        #     return render_template("sign-in.html")
        if pas!=passw:
            error="invalid password"
            return render_template("login.html",error=error)

        login_user(user)
        return redirect(url_for('dash'))

@app.route("/sign-in", methods=["GET","POST"])
def signup():
    error=None
    if request.method=="GET":
        return render_template("sign-in.html",error=error)
    if request.method=="POST":
        uname=request.form["username"]
        pas=request.form["password"]
        repas=request.form["re_password"]
        if '"' in uname or "'" in uname:
            error="Enter a valid username"
            return render_template("sign-in.html",error=error)
        if '"' in pas or "'" in pas:
            error="Enter a valid password"
            return render_template("sign-in.html",error=error)
        if pas!=repas:
            error="re-entered password do not match"
            return render_template("sign-in.html",error=error)
        new_user=Username(username=uname,password=pas)
        db.session.add(new_user)
        db.session.commit()
        return render_template("login.html",error=error)

@app.route("/logout",methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/", methods=["GET","POST"])
@login_required
def dash():
    if request.method=="GET":
        deck=db.session.query(Deck).all()
        return render_template("dashboard.html",deck=deck)

@app.route("/deckmanagement", methods=["GET","POST"])
@login_required
def deck_manager():
    return render_template("deckManagement.html")

@app.route("/createdeck", methods=["GET","POST"])
@login_required
def createDeck():
    message=None
    if request.method=="GET":
        return render_template("CreateDeck.html")
    if request.method=="POST":
        
        dname=request.form["deck_name"]
        if "'" in dname or '"' in dname:
            message="Enter a Valid deck name"
            return render_template("CreateDeck.html",msg=message)
        d=db.session.query(Deck).filter(Deck.deck_name==dname).first()
        if d is not None:
            message="Deck already Exixst"
            return render_template("CreateDeck.html",msg=message)
        new_deck=Deck(deck_name=dname,score='0',time="-")
        db.session.add(new_deck)
        db.session.commit()
        return redirect("/")

@app.route("/deldeck",methods=["GET","POST"])
@login_required
def deldeck():
    message=None
    if request.method=="GET":
        return render_template("deldeck.html")
    else:
        name=request.form['deck_name']
        if "'" in name or '"' in name:
            message="Enter a Valid deck name"
            return render_template("deldeck.html",msg=message)
        deck=db.session.query(Deck).filter(Deck.deck_name==name).first()
        db.session.delete(deck)
        db.session.commit()
        return redirect("/")

@app.route("/review/<int:id>",methods=["GET","POST"])
@login_required
def review(id):
    global deckid
    deckid=id
    if request.method=="GET":
        card=db.session.query(Deck_Card).filter(Deck_Card.deck_id==id).all()
        l=[]
        for c in card:
            l.append(c.card_id)
        d={}
        s={}
        for i in l:
            ele=db.session.query(Card).filter(Card.Card_id==i).first()
            d[ele.card_front]=ele.card_back
            s[ele.card_front]=ele.score
        print(s)
        now=datetime.now()
        current_time=now.strftime('%H:%M:%S')
        deck=db.session.query(Deck).filter(Deck.deck_id==id).first()
        deck.time=current_time
        db.session.commit()
        x=json.dumps(d)
        y=json.dumps(s)
        return render_template("review.html",data=x,deck=deck,score=y)

@app.route("/score/<string:avgs>",methods=["POST"])
def score(avgs):
    global deckid
    sc=json.loads(avgs)
    scor=sc['score']
    deck=db.session.query(Deck).filter(Deck.deck_id==deckid).first()
    deck.score=str(scor)
    db.session.commit()
    return "success"

@app.route("/cardscore/<string:cscore>",methods=["POST"])
def cscore(cscore):
    global deckid
    sc=json.loads(cscore)
    print(sc)
    scor=sc['difficulty']
    card_front=sc['card_front']
    card_back=sc['card_back']
    
    card=db.session.query(Card).filter(Card.card_front==card_front,Card.card_back==card_back).first()
    card.score=scor
    db.session.commit()
    return "success"

@app.route("/addcard",methods=["GET","POST"])
@login_required
def add_card():
    if request.method=="GET":
        return render_template("AddCard.html")
    if request.method=="POST":
        deck=request.form["deck_name"]
        cardf=request.form["card_front"]
        cardb=request.form["card_back"]
        deck_id=db.session.query(Deck).filter(Deck.deck_name==deck).first()
        if(deck_id==None):
            message="Enter Valid Deck Name"
            return render_template("AddCard.html",msg=message)
        if '"' in cardf or "'" in cardf:
            message="Enter Valid card Front"
            return render_template("AddCard.html",msg=message)
        if '"' in cardb or "'" in cardb:
            message="Enter Valid card Back"
            return render_template("AddCard.html",msg=message)
        c=db.session.query(Card).filter(Card.card_front==cardf,Card.card_back==cardb).first()
        if c is not None:
            message="Card Already Exist"
            return render_template("AddCard.html",msg=message)
        new_card=Card(card_front=cardf,card_back=cardb, score='-')
        db.session.add(new_card)
        db.session.commit()
        card_id=db.session.query(Card).filter(Card.card_front==cardf,Card.card_back==cardb).first()

        
        new_dc=Deck_Card(card_id=card_id.Card_id,deck_id=deck_id.deck_id)
        db.session.add(new_dc)
        db.session.commit()
        message='Added'
        return render_template("AddCard.html",msg=message)

@app.route("/delcard",methods=["GET","POST"])
@login_required
def delcard():
    msg=None
    if request.method=="GET":
        return render_template("delcard.html",msg=msg)
    else:
        deck=request.form["deck_name"]
        cardf=request.form["card_fname"]
        cardb=request.form["card_bname"]
        card=db.session.query(Card).filter(Card.card_front==cardf, Card.card_back==cardb).first()
        deck_id=db.session.query(Deck).filter(Deck.deck_name==deck).first()
        if(deck_id==None):
            message="Enter Valid Deck Name"
            return render_template("delcard.html",msg=message)
        if card:
            if '"' in cardf or "'" in cardf:
                message="Enter Valid card Front"
                return render_template("delcard.html",msg=message)
            if '"' in cardb or "'" in cardb:
                message="Enter Valid card Back"
                return render_template("delcard.html",msg=message)
            message='Deleted'
            db.session.delete(card)
            db.session.commit()
            return render_template("delcard.html",msg=message)
        else:
            message="Card Not Found"
            return  render_template("delcard.html",msg=message)




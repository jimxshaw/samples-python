from flask import Flask, render_template, abort, jsonify

from model import db

app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("welcome.html",
                           cards=db)


@app.route("/cards/<int:index>")
def card_view(index):
    try:
        card = db[index]
        return render_template("card.html",
                               card=card,
                               index=index,
                               max_index=len(db) - 1)
    except IndexError:
        abort(404)


@app.route("/add_card")
def add_card():
    return render_template("add_card.html")


@app.route("/api/cards/")
def api_card_list():
    return jsonify(db)


@app.route("/api/cards/<int:index>")
def api_card_detail(index):
    try:
        return db[index]
    except IndexError:
        abort(404)

import json


def load_db():
    with open("flashcards_db.json") as file:
        return json.load(file)


db = load_db()

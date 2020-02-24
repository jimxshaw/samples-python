import json


def load_db():
    with open("flashcards_db.json") as file:
        return json.load(file)


def save_db():
    with open("flashcards_db.json", "w") as file:
        return json.dump(db, file)

db = load_db()


from flask import Flask, jsonify, request
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import json
import os
from pathlib import Path

app = Flask(__name__)

DATA_FILE = Path(__file__).with_name("data.json")

mongo_client = None


def get_todo_collection():
    global mongo_client

    mongo_uri = os.getenv("MONGODB_URI")

    if not mongo_uri:
        raise RuntimeError("MONGODB_URI is not configured")

    if mongo_client is None:
        mongo_client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=5000
        )

    return mongo_client["flask_todo_db"]["todo_items"]


@app.route("/")
def home():
    return "Flask application is running!"


@app.route("/api", methods=["GET"])
def get_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return jsonify(data)


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"message": "Valid JSON required"}), 400

    item_name = data.get("itemName")
    item_description = data.get("itemDescription")

    if not isinstance(item_name, str) or not item_name.strip():
        return jsonify({"message": "Item Name is required"}), 400

    if not isinstance(item_description, str) or not item_description.strip():
        return jsonify({"message": "Item Description is required"}), 400

    todo_item = {
        "itemName": item_name.strip(),
        "itemDescription": item_description.strip()
    }

    try:
        collection = get_todo_collection()
        result = collection.insert_one(todo_item)

        return jsonify({
            "message": "To-Do item submitted successfully",
            "insertedId": str(result.inserted_id)
        }), 201

    except (RuntimeError, PyMongoError):
        app.logger.exception("MongoDB submission failed")
        return jsonify({
            "message": "Unable to save To-Do item"
        }), 503


if __name__ == "__main__":
    app.run(debug=True)

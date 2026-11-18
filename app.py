from flask import Flask, jsonify
import json
from pathlib import Path

app = Flask(__name__)

DATA_FILE = Path(__file__).with_name("data.json")

@app.route("/")
def home():
    return "Flask application is running!"

@app.route("/api", methods=["GET"])
def get_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

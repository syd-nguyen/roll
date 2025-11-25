from flask import Flask, render_template, request, jsonify
from storage import append_json_line
from pymongo import MongoClient
import os

app = Flask(__name__)

client = MongoClient("mongodb+srv://sydnguyen:uva343TL%23%2B%23%2B@cluster0.9srpoaq.mongodb.net/?appName=Cluster0")
db = client["main"]
events = db["events"]

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.post("/api/send-event-to-mongo")
def echo():
    data = request.get_json(silent=True) or {}
    append_json_line(data)
    events.insert_one(data)
    return jsonify({"testing": 123}), 200


if __name__ == "__main__":
    app.run()
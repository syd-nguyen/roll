from flask import Flask, render_template, request, jsonify
from storage import append_json_line
from pymongo import MongoClient
from pydantic import ValidationError
from models import EventSubmission, EventSubmissionRecord
from datetime import datetime, timezone
import os

app = Flask(__name__)

client = MongoClient("mongodb+srv://sydnguyen:uva343TL%23%2B%23%2B@cluster0.9srpoaq.mongodb.net/?appName=Cluster0") # remember to add this as an environment variable later
db = client["main"]
events = db["events"]

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.post("/api/send-event-to-mongo")
def sendEventToMongo():
    formData = request.get_json(silent=True) # or {}
    print(formData)
    if formData is None:
        return
    
    try:
        validatedFormData = EventSubmission(**formData)
        print(validatedFormData)
    except ValidationError as ve:
        print(jsonify({"error": "validation error", "detail": ve.errors()}))
        return jsonify({"error": "validation error", "detail": ve.errors()}), 422
    
    eventRecord = EventSubmissionRecord(
        **validatedFormData.dict(),
        received_at=datetime.now(timezone.utc)
    )

    append_json_line(eventRecord.dict())
    events.insert_one(validatedFormData.dict())
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run()
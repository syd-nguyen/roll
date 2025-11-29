from flask import Flask, render_template, request, jsonify, redirect, url_for
from storage import append_json_line
from pymongo import MongoClient
from pydantic import ValidationError
from models import EventSubmission, EventSubmissionRecord
from datetime import datetime, timezone
from hashlib import sha256
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

    formData = request.get_json(silent=True) # silent=True suppresses warnings and returns None if there is an error
    if formData is None:
        return
    
    # validate form data and throw error if applicable
    try:
        validatedFormData = EventSubmission(**formData)
    except ValidationError as ve:
        print("Error:", ve.errors())
        return jsonify({"error": "validation error", "detail": ve.errors()}), 422
    
    received = datetime.now(timezone.utc)
    strToHash = validatedFormData.dict()['eventName'] + validatedFormData.dict()['eventDesc'] # to do, change this to something that doesn't change, like the time of the event maybe idk
    hashedStr = hash(strToHash)

    # add additional information for record keeping
    eventRecord = EventSubmissionRecord(
        **validatedFormData.dict(),
        receivedAt = received,
        eventHash = hashedStr,
        eventId = hashedStr[:6] # id is first six characters of hash
    )

    append_json_line(eventRecord.dict())
    #events.insert_one(eventRecord.dict()) UNCOMMENT THIS LATERRRRR THIS IS VERY IMPORTANT
    
    return jsonify({"status": "ok"}), 200

@app.route('/<eventId>')
def getEventPage(eventId):
    # get event from Mongo using its id
    event = events.find_one({'eventId' : eventId})
    # render it
    if (event is not None):
        return render_template('event.html', eventName = event['eventName'])

def hash(str):
    return sha256(str.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    app.run()
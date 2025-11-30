from flask import Flask, render_template, request, jsonify, redirect, url_for
from storage import append_json_line
from pymongo import MongoClient
from pydantic import ValidationError
from models import EventSubmission, EventSubmissionRecord, CarSubmission
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

    eventRecordDict = eventRecord.dict()
    eventRecordDict.update({'cars': []})

    # add to Mongo database along with empty array of cars
    append_json_line(eventRecordDict)
    events.insert_one(eventRecordDict)
    
    return jsonify({"status": "ok"}), 200

@app.get('/<eventId>')
def getEventPage(eventId):
    # get event from Mongo using its id
    event = events.find_one({'eventId' : eventId})
    # render it
    if (event is not None):
        return render_template('event.html', eventName = event['eventName'])
    return render_template('eventDNE.html', eventId = eventId)
    
@app.post('/api/send-car-to-mongo/<eventId>')
def sendCarToMongo(eventId):

    formData = request.get_json(silent=True) # silent=True suppresses warnings and returns None if there is an error
    if formData is None:
        return
    
    # validate form data and throw error if applicable
    try:
        validatedFormData = CarSubmission(**formData)
    except ValidationError as ve:
        print("Error:", ve.errors())
        return jsonify({"error": "validation error", "detail": ve.errors()}), 422

    # get corresponding event from Mongo using eventId and insert car into that event
    events.update_one( { "eventId": eventId }, { "$push": { "cars": validatedFormData.dict() } })

    return jsonify({"status": "ok"}), 200

@app.get('/api/get-cars-for-event/<eventId>')
def testing(eventId):
    event = getEvent(eventId)
    if (event is not None):
        return event['cars']
    else: return jsonify({'error': 'no event found'})

def hash(str):
    return sha256(str.encode('utf-8')).hexdigest()

def getEvent(eventId):
    return events.find_one({'eventId' : eventId})

if __name__ == "__main__":
    app.run()
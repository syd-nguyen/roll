from flask import Flask, render_template, request, jsonify, redirect, url_for
from storage import append_json_line
from pymongo import MongoClient
from pydantic import ValidationError
from models import EventSubmission, EventSubmissionRecord, CarSubmission, RiderSubmission
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
    validatedFormDataDict = validatedFormData.dict()

    datetimeStr = str(validatedFormDataDict['eventDatetime']) # this is in the format yyyy-mm-dd hh:mm:ss but javascript has it in the format yyyy-mm-ddThh:mm
    datetimeStr = datetimeStr[:10] + 'T' + datetimeStr[11:16]
    
    strToHash = validatedFormDataDict['eventName'] + validatedFormDataDict['eventDesc'] + datetimeStr; # to do, change this to something that doesn't change, like the time of the event maybe idk
    print(strToHash)
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
        return render_template('event.html', eventName = event['eventName'], eventDesc = event['eventDesc'])
    return render_template('eventDNE.html', eventId = eventId)
    
@app.post('/api/send-car-to-mongo/<eventId>')
def sendCarToMongo(eventId):

    formData = request.get_json(silent=True)
    if formData is None:
        return
    
    # validate form data and throw error if applicable
    try:
        validatedFormData = CarSubmission(**formData)
    except ValidationError as ve:
        print("Error:", ve.errors())
        return jsonify({"error": "validation error", "detail": ve.errors()}), 422
    
    carDict = validatedFormData.dict()
    carDict.update({'riders': []})

    # get corresponding event from Mongo using eventId and insert car into that event
    events.update_one( { "eventId": eventId }, { "$push": { "cars": carDict } })

    return jsonify({"status": "ok"}), 200

@app.get('/api/get-cars-for-event/<eventId>')
def getCarsForEvent(eventId):
    event = getEvent(eventId)
    if event is not None:
        return event['cars']
    else: return []

@app.post('/api/send-rider-to-mongo/<eventId>/<driverName>') # this finds the car via the driver name but it could be changed to be by an id
def sendRiderToMongo(eventId, driverName):

    formData = request.get_json(silent=True)
    if formData is None:
        return
    
    # validate form data and throw error if applicable
    try:
        validatedFormData = RiderSubmission(**formData)
    except ValidationError as ve:
        print("Error:", ve.errors())
        return jsonify({"error": "validation error", "detail": ve.errors()}), 422
    
    # this is kind of a goofy way to update the embedded documents but it works so yea :)

    carsToUpdate = getEventCars(eventId, driverName) # this is an array of documents (which is also embedded within an event document)

    for car in carsToUpdate: # each car is a document with an array of rider documents
        if car['driverName'] == driverName:

            ridersToUpdate = car['riders'] # this is an array of documents
            ridersToUpdate.append(validatedFormData.dict())
            car.update({'riders' : ridersToUpdate})

            takenSeatsToUpdate = car['takenSeats']
            takenSeatsToUpdate = takenSeatsToUpdate + 1
            car.update({'takenSeats': takenSeatsToUpdate})
    
    events.update_one( { "eventId": eventId }, { "$set" : { "cars": carsToUpdate }})

    return jsonify({"status": "ok"}), 200

@app.post('/api/remove-car-from-mongo/<eventId>/<driverName>')
def removeCarFromMongo(eventId, driverName):
    carsToUpdate = getEventCars(eventId, driverName) # this is an array of documents / dictionaries (which is also embedded within an event document)

    for car in carsToUpdate: # each car is a document with an array of rider documents
        if car['driverName'] == driverName:
            carsToUpdate.remove(car)
    
    events.update_one( { "eventId": eventId }, { "$set" : { "cars": carsToUpdate }})

    return jsonify({"status": "ok"}), 200

@app.post('/api/remove-rider-from-mongo/<eventId>/<driverName>/<riderName>')
def removeRiderFromMongo(eventId, driverName, riderName):

    carsToUpdate = getEventCars(eventId, driverName)

    for car in carsToUpdate:
        if car['driverName'] == driverName:
            
            ridersToUpdate = car['riders']

            for rider in ridersToUpdate:
                if rider['riderName'] == riderName:

                    ridersToUpdate.remove(rider)

                    takenSeatsToUpdate = car['takenSeats']
                    takenSeatsToUpdate = takenSeatsToUpdate - 1
                    car.update({'takenSeats': takenSeatsToUpdate})

            car.update({'riders' : ridersToUpdate})
    
    events.update_one( { "eventId": eventId }, { "$set" : { "cars": carsToUpdate }})

    return jsonify({"status": "ok"}), 200

def hash(str):
    return sha256(str.encode('utf-8')).hexdigest()

def getEvent(eventId):
    return events.find_one({'eventId' : eventId})

def getEventCars(eventId, driverName):
    return getEvent(eventId)['cars']

if __name__ == "__main__":
    app.run(debug=True)
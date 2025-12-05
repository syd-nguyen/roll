# 🚗 roll

## ⭐ Executive Summary

### ❔ Problem

_It's a busy world out there! There's things to do, places to be, people to see, and more... but! it's better when it's done together._

Carpooling is the manifestation of this. In many contexts, but especially in college, many people have a place to be but not all of those people have a car. Carpooling helps them get where they need to go more efficiently. To coordinate this, college students will often create "rideboards." These are usually just spreadsheets, which works but is not the best system for a few reasons:

* __Someone has to make the board:__ Whether it's someone who haphazardly throws it together or someone who spends a whole third-hour on it, someone has to make the board. They have sit down and make a spreadsheet and add headers and type up everything.
* __The formatting varies:__ Because a different person makes the board everytime, it always turns out different. Sometimes passengers have to put their phone number, sometimes they don't, sometimes they have to put their pickup location, sometimes they don't, etc.
* __The link is long and not guaranteed to work:__ A spreadsheet link is something like "https://docs.google.com/spreadsheets/d/234w5sb8hcyjagsfjk12jgk-jn391o2i256351hndh21yy3989213/edit?usp=sharing" which is long and unwieldy. The permissions on the sheet might also be set incorrectly, so the link might have to be edited and fixed.

### ✔️ Solution

_roll_ is a website that makes creating rideboards simple and easy. Creating a rideboard for an event is a breeze — just fill out a few fields and click a button! Each event has its own page with a shareable link in the form `roll.xyz/######` where `######` is a unique, alphanumeric id. On that page, users can add and delete cars and riders as necessary, as well as see all existing cars and riders.

## System Overview

### Course Concepts

_roll_ makes use of the following course concepts:

* GitHub version control
* Docker containerization
* Flask app creation
* NoSQL data in MongoDB
* Pydantic data validation

### Architecture Diagram

![image](../assets/diagram.png)

### Data / Models / Services

Data in _roll_ is stored in a MongoDB database. All events are stored in one container. Each event is a document with the following information:

* name
* description
* location
* datetime
* hash and unique id
* cars

The `cars` for an event is an array of documents, each of which have:

* driver name
* total number of seats
* current number of filled seats
* riders

The `riders` for an event is also an array of documents. Each rider document has:

* rider name
* rider phone number

The data is created when users create events and is thus of a variable size. All data is kept private.

## How to Run (Local)

### Docker

_roll_ is available as a public Docker image at [this Docker Hub repository](https://hub.docker.com/repository/docker/cvv8cb/roll/general). To run the image, execute the following command:

`docker run -it cvv8cb/roll:latest`


## Design Decisions

* GitHub version control
* Docker containerization
* Flask app creation
* NoSQL data in MongoDB
* Pydantic data validation

### Why these Concepts

### Tradeoffs

### Security / Privacy

### Ops


## Results & Evaluation

### Sample Outputs

### Performance Notes & Resource Footprints (optional, prob won't need)

### Validation Tests


## What's Next

### Planned Improvements, Refactors, and Features

* better phone number validation
* better hashing, some 6 digits might be the same so just use the second 6 digits etc.

## Links

### Github Repo

### Public Cloud App

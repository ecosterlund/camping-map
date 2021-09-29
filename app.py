# 1. import Flask and dependencies
from flask import Flask, jsonify, render_template
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import sqlite3
from pathlib import Path
import pandas as pd
import psycopg2
import json
import requests
import sqlite3
from sqlite3 import Error
import csv

# Master mapbox api key only works when requests originate from Heroku.  The following mapbox key is for testing or debugging purposes
# pk.eyJ1IjoiZWNvc3Rlcmx1bmQiLCJhIjoiY2tucDZxMWljMDBnaTJwbnVhaWV1YWxheiJ9.JVj5mJ67soe4MtmfktHtvw


# backend retival of API information from parks dept, api calls need to be back end to prevent lost api keys
# US gov parks dept urls and api key
parksURL = "https://developer.nps.gov/api/v1/parks?limit=1000&api_key="
campsURL = "https://developer.nps.gov/api/v1/campgrounds?limit=1000&api_key="
usaParksKEY = "xsZZUPjjCHE5X8sIHnoML8wsrWHWHKblRq6WDwjV"

# requests from the parks api and returns a json, saving that json to file for both camps and parks
parksData = requests.get(parksURL + usaParksKEY)
parksJson = parksData.json()

with open('static/geojson/parksJSON.json', 'w') as json_file:
    json.dump(parksJson, json_file)


campsData = requests.get(campsURL + usaParksKEY)
campsJson = campsData.json()

with open('static/geojson/campsJSON.json', 'w') as json_file:
    json.dump(campsJson, json_file)


#################################################
# Flask Setup
#################################################
# Create an app
app = Flask(__name__)

#################################################
# Route to homepage: index.html
#################################################
# Define what to do when a user hits the index route
@app.route("/")
def welcome():

    return render_template("index.html")

#################################################
# Routes to other html files: story.html and team.html
#################################################
@app.route("/story")
def story():

    return render_template("story.html")

@app.route("/team")
def team():

    return render_template("team.html")


#################################################
#End of App
#################################################    

if __name__ == "__main__":
    app.run(debug=True)


# The following is legacy code, allows heat mapping section to be written from a database

# ####Creating the engine
# engine = create_engine('sqlite://', echo=False)

# #################################################
# # Database Setup
# #################################################
# # Path to sqlite---------------- IF THIS DOESN'T WORK CHANGE PORT TO 5433
# database_path = "postgresql://postgres:postgres@localhost:5433/firemap_db"

# # Create an engine that can talk to the database
# engine = create_engine(database_path)

# # Query All Records in the the Database
# latlongdata = engine.execute("SELECT lat, lng FROM firemap")



#################################################
# Route to obtain firemap data from firemap_db
#################################################
# @app.route("/jsonify")
# def firecoordinates():
#     #################################################
#     # Getting fire data into json object
#     #################################################
#     res = engine.execute("SELECT lat, lng from firemap")
#     data = json.dumps([dict(r) for r in res])
#     ######-----------------CURRENTLY WORKING TO READ CSV WITHOUT DATABASE-------######
#     # csvfile = open('ETL/firecoord.csv', 'r')
#     # jsonfile = open('wildlandjson.json', 'w')
#     # reader = csv.DictReader(csvfile, jsonfile)
#     # for row in reader:
#     #     json.dump(row, jsonfile)
#     #     jsonfile.write('/n')
#     return data

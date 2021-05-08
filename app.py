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
import sqlite3
from sqlite3 import Error


####Creating the engine
engine = create_engine('sqlite://', echo=False)

#################################################
# Database Setup
#################################################
# Path to sqlite---------------- IF THIS DOESN'T WORK CHANGE PORT TO 5433
database_path = "postgres://postgres:postgres@localhost:5433/firemap_db"

# Create an engine that can talk to the database
engine = create_engine(database_path)

# Query All Records in the the Database
latlongdata = engine.execute("SELECT lat, lng FROM firemap")

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
# Route to obtain firemap data from firemap_db
#################################################
@app.route("/jsonify")
def firecoordinates():
    #################################################
    # Getting fire data into json object
    #################################################
    res = engine.execute("SELECT lat, lng from firemap")
    data = json.dumps([dict(r) for r in res])

    return data


#################################################
#End of App
#################################################    
if __name__ == "__main__":
    app.run(debug=True)

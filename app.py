# 1. import Flask and dependencies
from flask import Flask, jsonify, render_template
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import sqlite3
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import json


#################################################
# Database Setup
#################################################
# Path to sqlite
database_path = "postgres://postgres:postgres@localhost:5433/firemap_db"

# Create an engine that can talk to the database
engine = create_engine(database_path)

# Query All Records in the the Database
latlongdata = engine.execute("SELECT lat, lng FROM firemap")

#################################################
# Flask Setup
#################################################
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)
# 3. Define what to do when a user hits the index route ------------------------- NEED TO RENDER TEMPLATE HERE
@app.route("/")
def welcome():

    return render_template("index.html")

@app.route("/jsonify")
def firecoordinates():
    #################################################
    # Getting fire data into json object
    #################################################
    res = engine.execute("SELECT lat, lng from firemap")
    data = json.dumps([dict(r) for r in res])

    return data

#End of App
if __name__ == "__main__":
    app.run(debug=True)

# 1. import Flask and dependencies
from flask import Flask
from flask import Flask, jsonify
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

# Path to sqlite
database_path = "postgres://postgres:postgres@localhost:5433/firemap_db"

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
# Getting fire data into json object
#################################################
#Creating empty arrays for lat and long fire values
lat = []
long = []

#Grabbing data from database
latdata = engine.execute("SELECT lat FROM firemap")
longdata = engine.execute("SELECT lng FROM firemap")

#Append latitude data from db to the empty lat array
for record in latdata:
    lat.append(record)

#Append longitude data from db to the empty long array
for record in longdata:
    long.append(record)

#Defining dictionary and key values
data = {'Lat': lat,
        'Lng': long
        }

#Converting data variable into pandas dataframe (df)
df = pd.DataFrame(data, columns = ['Lat', 'Lng'])

#Converting pandas dataframe(df) into json file
dfjson = df.to_json()

#################################################
# Flask Setup
#################################################
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)
# 3. Define what to do when a user hits the index route
@app.route("/")
def welcome():

    return print("return index.html here")

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

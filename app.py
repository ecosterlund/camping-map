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
# Flask Setup
#################################################
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)
# 3. Define what to do when a user hits the index route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/story<br/>"
        f"/jsonify"
    )
@app.route("/jsonify")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all Fire Coordinates"""
    # # Query All Records in the the Database and jsonify
    latdata = engine.execute("SELECT lat FROM firemap")
    longdata = engine.execute("SELECT lng FROM firemap")

    data = {'Lat': latdata,
        'Long': longdata
        }
    df = pd.DataFrame(data, columns = ['Lat', 'Lng'])

    my_dictionary = df.to_dict()
    ####--------WORKING ON TRANSFERRING LIST OF ARRAYS INTO DICT OBJECT --------
    # d1=zip(latdata,longdata)
    # print (d1)#Output:<zip object at 0x01149528>
    # #Converting zip object to dict using dict() contructor.
    # print (dict(d1))

    # #Create loop to make array a dictionary
    # latlongdict = {"lat" : latdata,"long": longdata}
    # for entry in latlongdata:
    #     latlongdict["lat"].append(latlongdata[entry])
    #     # latlongdict["long"].append(latlongdata[entry])	
    # print(latlongdict)



    # print(latlongdata)
    
    return jsonify(my_dictionary)

# @app.route("/jsonify")
# def Fires():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)
#     """Return a list of Fire data including the name, age, and sex of each Fire"""
#     # Query all Fires
#     results = session.query(Fire.name, Fire.age, Fire.sex).all()
#     session.close()
#     # Create a dictionary from the row data and append to a list of all_Fires
#     all_Fires = []
#     for name, age, sex in results:
#         Fire_dict = {}
#         Fire_dict["name"] = name
#         Fire_dict["age"] = age
#         Fire_dict["sex"] = sex
#         all_Fires.append(Fire_dict)
#     return jsonify(all_Fires)

if __name__ == "__main__":
    app.run(debug=True)

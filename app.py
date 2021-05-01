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
def firecoordinates():
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
            'Long': long
            }
    #Converting data variable into pandas dataframe (df)
    df = pd.DataFrame(data, columns = ['Lat', 'Lng'])
    #Converting the pandas dataframe into a dictionary variable (fire_dict)
    fire_dict = df.to_dict()
    df = fire_dict
    #Dependency (used in an example, may be able to define outside of function)
    import json
    #Converting pandas dataframe(df) into json file
    class JSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if hasattr(obj, 'to_json'):
                return obj.to_json(orient='records')
            return json.JSONEncoder.default(self, obj)
    #!-----ERROR OCCURS WHEN RUNNING NEXT LINE OF CODE (When running the jupyter notebook this error occurs: 
    #!-----(TypeError: Object of type 'RowProxy' is not JSON serializable)-----!
    with open('result.json', 'w') as fp:
        json.dump({'1':df,'2':df}, fp, cls=JSONEncoder)
    #Load the coordinate data into a json file called "result.json"
    json.load(open('result.json')
    #Read the json that has been loaded with the pandas dataframe (df)
    pd.read_json(json.load(open('result.json'))['1'])

    # # Create our session (link) from Python to the DB
    # session = Session(engine)
    # #"""Return a list of all Fire Coordinates"""
    # # # Query All Records in the the Database and jsonify
    # latdata = engine.execute("SELECT lat FROM firemap")
    # longdata = engine.execute("SELECT lng FROM firemap")

    # data = {'Lat': latdata,
    #     'Long': longdata
    #     }
    # df = pd.DataFrame(data, columns = ['Lat', 'Lng'])

    # fire_dict = df.to_dict()
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
    
    # return jsonify(fire_dict)

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

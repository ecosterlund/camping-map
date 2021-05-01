# 1. import Flask and dependencies
from flask import Flask
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

#################################################
# Database Setup
#################################################
engine = fire_db.engine.execute("SQL/fire_db.sql")

# engine = create_engine("sqlite:///SQL/fire_db.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Fire = Base.classes

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
@app.route("/story")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all Fire Coordinates"""
    # Query all Fires
    results = session.query(Fire.lat, Fire.lng).all()
    session.close()
    # Convert list of tuples into normal list
    fire_coord = list(np.ravel(results))
    print(fire_coord)
    return jsonify(fire_coord)

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

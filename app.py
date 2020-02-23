# The first thing we’ll need to import is datetime, NumPy, and Pandas. We assign each of these an alias so we can easily reference them later
import datetime as dt
import numpy as np
import pandas as pd

# Now let’s get the dependencies we need for SQLAlchemy, which will help us access our data in the SQLite database
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Now let’s get the dependencies we need for SQLAlchemy, which will help us access our data in the SQLite database
from flask import Flask, jsonify

# We’ll set up our database engine for the Flask application
engine = create_engine("sqlite:///hawaii.sqlite")

# The create_engine() function allows us to access and query our SQLite database file. Now let’s reflect the database into our classes
Base = automap_base()

# Reflect the database
Base.prepare(engine, reflect=True)

# With the database reflected, we can save our references to each table. Again, they’ll be the same references as the ones we wrote earlier in this module. We’ll create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to our database
session = Session(engine)

# This will create a Flask application called “app.”
app = Flask(__name__)

# Define the welcome route
@app.route("/")

@app.route("/")
def welcome():
    test = (f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>" 
        f"/api/v1.0/temp/start/end")
    return (test)

# Define precipitation route
@app.route("/api/v1.0/precipitation")

def precipitation():
        prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        precipitation = session.query(measurement.date, measurement.prcp).\
		filter(measurement.date >= prev_year).all()
        precip = {date: prcp for date, prcp in precipitation}
        return jsonify(precip)

# Define stations route
@app.route("/api/v1.0/stations")

def stations():
        results = session.query(station.station).all()
        stations = list(np.ravel(results))
        return jsonify(stations)

# Define tobs route
@app.route("/api/v1.0/tobs")

def temp_monthly():
        prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        results = session.query(measurement.tobs).\
            filter(measurement.station == 'USC00519281').\
            filter(measurement.date >= prev_year).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

    if not end: 
        results = session.query(*sel).\
            filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
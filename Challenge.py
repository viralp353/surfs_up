# import depencies:
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask,jsonify
from sqlalchemy import extract
import app

# create a engine:
engine = create_engine("sqlite:///hawaii.sqlite")
#create base:
Base = automap_base()
#reflact schema from the tables:
Base.prepare(engine, reflect=True)
# add class:
Measurement = Base.classes.measurement
Station = Base.classes.station
# create session link to data base:
session = Session(engine)
app = Flask(__name__)

# Route for welcome page:
@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    /api/v1.0/june
    /api/v1.0/december
    ''')

# create a route for percipatation:
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
	filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

#create Stations Route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# create Monthly Temperature Route:
@app.route("/api/v1.0/tobs")
def temp_monthly():

   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   results = session.query(Measurement.tobs).\
       filter(Measurement.station == 'USC00519281').\
       filter(Measurement.date >= prev_year).all()
   temps = list(np.ravel(results))
   return jsonify(temps=temps)

#Statistics Route
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
   return jsonify(temps=temps)


#create route for june:
@app.route("/api/v1.0/june")
def june():
    june = session.query(Measurement.date, Measurement.prcp,Measurement.tobs,Measurement.station).filter( extract('month', Measurement.date) == 6).all()
    temp = list(np.ravel(june))
    return jsonify(temp=temp)


#create route for june:
@app.route("/api/v1.0/december")
def dec():
    dec = session.query(Measurement.date, Measurement.prcp,Measurement.tobs,Measurement.station).filter( extract('month', Measurement.date) == 12).all()
    temperature = list(np.ravel(dec))
    return jsonify(temperature=temperature)

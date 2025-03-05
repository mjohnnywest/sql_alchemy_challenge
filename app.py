# Import the dependencies.
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect
from datetime import timedelta
app = Flask(__name__)


#################################################
# Database Setup
#################################################

# Loading and mapping the database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with= engine)

#saving db tables
measurement = Base.classes.measurement
station = Base.classes.station

#creating an engine from database
session = Session(engine)


#homepage
@app.route("/")
def home():
    return "This is the homepage of the climate app <br>\
        Here are the pages you can visit <br>\
        <br>\
        /api/v1.0/precipitation returns last 12 months of precipitation data as a dictionary <br>\
        <br>\
        /api/v1.0/stations contains JSON of  station names <br>\
        <br>\
        /api/v1.0/start-date JSON of Max, Min Avg temp after date, at most frequent station <br>\
        <br>\
        /api/v1.0/start-date/end-date JSON of Max, Min Avg between 2 dates at most frequent station <br>\
        <br>\
        Note: Date format is as follows: YYYY-MM-DD"

#################################################
# Flask Routes
#################################################

#dict of precip by date
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_date = session.query(measurement.date, measurement.prcp).filter(measurement.date>="2016-08-18").all()
    prcp_date = dict(prcp_date)
    return jsonify(prcp_date)

#Json list of station names
@app.route("/api/v1.0/stations")
def stations():
    station_list = []
    station = session.query(measurement.station).group_by(measurement.station).all()
    for x in station:
        station_list.append(x[0])
    return jsonify(station_list)

#temp taking start date only
@app.route("/api/v1.0/<start>")
def temp_start(start):
    max_temp = session.query(measurement.tobs, func.max(measurement.tobs)).\
    filter(measurement.date>= start, measurement.station=="USC00519281").all()
    min_temp = session.query(measurement.tobs, func.min(measurement.tobs)).\
    filter(measurement.date>=start, measurement.station=="USC00519281").all()
    avg_temp = session.query(measurement.tobs, func.avg(measurement.tobs)).\
    filter(measurement.date>=start, measurement.station=="USC00519281").all()
    return jsonify(max_temp[0][1],min_temp[0][1],avg_temp[0][1])

#temp taking start and end date
@app.route("/api/v1.0/<start>/<end>")
def temp_range(start,end):
    max_temp = session.query(measurement.tobs, func.max(measurement.tobs)).\
    filter(measurement.date>= start, measurement.date<= end, measurement.station=="USC00519281").all()
    min_temp = session.query(measurement.tobs, func.min(measurement.tobs)).\
    filter(measurement.date>=start, measurement.date<= end, measurement.station=="USC00519281").all()
    avg_temp = session.query(measurement.tobs, func.avg(measurement.tobs)).\
    filter(measurement.date>=start, measurement.date<= end, measurement.station=="USC00519281").all()
    return jsonify(max_temp[0][1],min_temp[0][1],avg_temp[0][1])


if __name__ == "__main__":
    app.run(debug = True)
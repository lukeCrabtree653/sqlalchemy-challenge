import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)



@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return ( f"Homepage<br/>"
    f"Available Routes:<br/>"   
    f"/api/v1.0/precipitation<br/>"  
    f"/api/v1.0/stations<br/>" 
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/<start><br/>" 
    f'/api/v1.0/<start>/<end>')



@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.prcp).all()
    session.close()
    prcpjson = list(np.ravel(results))
    return jsonify(prcpjson)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.name).all()
    session.close()
    stationjson = list(np.ravel(results))
    return jsonify(stationjson)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').all()
    session.close()
    tobsjson = list(np.ravel(results))
    return jsonify(tobsjson)


@app.route("/api/v1.0/<start>")
def startRoute(start=None):
   session = Session(engine)
   results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
   session.close()
   startjson = list(np.ravel(results))
   return jsonify(startjson)


@app.route("/api/v1.0/<start>/<end>")
def startEndRoute(start=None, end=None):
   session = Session(engine)
   results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()
   session.close()
   startjson = list(np.ravel(results))
   return jsonify(startjson)

if __name__ == "__main__":
    app.run(debug=True)

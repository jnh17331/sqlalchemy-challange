# Import the dependencies.
import sqlalchemy
from flask import Flask, jsonify
import datetime as dt
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

# reflect the tables

Base.classes.keys()

# Save references to each table

Measurement  = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def main():
        return (
            f"Welcome to my Hawaii Climate App :)</br>"
            f"Routes:</br>"
            f"/api/v1.0/precipitation</br>"
            f"/api/v1.0/stations</br>"
            f"/api/v1.0/tobs</br>"
            f"/api/v1.0/start</br>"
            f"/api/v1.0/start/end</br>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
        
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).order_by(Measurement.date).all()

    results_dict = dict(results)
    session.close()
    return jsonify(results_dict)


@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Measurement.station, func.count(Measurement.id)).\
            group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()

    stations_dict = dict(stations)
    session.close()
    return jsonify(stations_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    max_temp_obs = session.query(Measurement.station, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').all()

    tobs_dict = dict(max_temp_obs)
    session.close()
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def start(start):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                                func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    session.close()
    tobsall = []

    for min,avg,max in result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)
        
    return jsonify(tobsall)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    
    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
    end_date = dt.datetime.strptime(end, "%Y-%m-%d").date()

    
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    
    if result:
        # Create a list to store the temperature data
        tobsall = []

        
        for min_temp, avg_temp, max_temp in result:
            tobs_dict = {}
            tobs_dict["Min"] = min_temp
            tobs_dict["Average"] = avg_temp
            tobs_dict["Max"] = max_temp
            tobsall.append(tobs_dict)

        return jsonify(tobsall)
    else:
        
        return jsonify({"message": "No data found for the given date range."})


if __name__ == '__main__':
    app.run(debug=True)
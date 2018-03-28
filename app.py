#################################################
# import necessary libraries
#################################################
import pandas as pd
import os
import io
import json
import requests
import plotly.plotly
import getStateData
import getRegionData
import getSpeciesData
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from splinter import Browser
from bs4 import BeautifulSoup as bs

from flask import Flask, render_template, redirect, jsonify, request, url_for

import numpy as np
from PIL import Image
import tensorflow as tf
import keras
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from keras.applications.xception import (
    Xception, preprocess_input, decode_predictions
)


from sqlalchemy import Column, Float, Integer, String

import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import and_, or_
from sqlalchemy import func

# Create an engine connecting to the SQLite database file
engine = create_engine("sqlite:///birds.sqlite")

# Create a session
session = Session(bind = engine)

# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)
# Print all of the classes mapped to the Base
Base.classes.keys()

# Assign the measurement class to a variable called `Measurement`
Bird = Base.classes.species

# Assign the stations class to a variable called `StateCentroids`
StateCentroids = Base.classes.state_centroids

# Assign the stations class to a variable called `RegionCentroids`
RegionCentroids = Base.classes.region_centroids

# create instance of Flask app
app = Flask(__name__)
model = None
graph = None

def load_model():
    global model
    global graph
    model = keras.models.load_model("xception.h5")
    graph = K.get_session().graph

def prepare_image(image):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image_size = (299, 299)
    image = image.resize(image_size)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    return image

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#################################################
# route that renders index.html template
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/states")
def state():
    return render_template("states.html")

@app.route("/regional")
def regional():
    return render_template("regional.html")

@app.route("/distr")
def distr():
    return render_template("distr.html")

@app.route("/species")
def species():
    return render_template("species.html")

@app.route("/birdTable")
def birdTable():
    return render_template("birdTable.html")

# route that returns a list of sample names
@app.route('/siteData/<ST>')
def siteData(ST):
    stateData = getStateData.getStateData(ST)
    top10 = getStateData.getTop10(stateData)
    return top10

@app.route('/birdData/<ST>')
def birdData(ST):
    stateData = getStateData.getStateData(ST)
    birds = getStateData.getBirds(stateData)
    birdsj = eval(birds)

    results = session.query(Bird.Common_Name, Bird.Img_URL, Bird.Audio_URL, Bird.Info_URL)

    #Convert the query results to a Dictionary using date as the key and tobs as the value.
    data = {}

    # populate dict with rows from results
    for row in results:
        sp = str(row.Common_Name).lower()
        data[sp] = [row.Img_URL, row.Audio_URL, row.Info_URL]

    for bird in birdsj:
        sp = bird['comName'].lower()
        if sp in data.keys():
            bird['img'] = data[sp][0]
            bird['audio'] = data[sp][1]
            bird['link'] = data[sp][2]
        else:
            bird['img'] = 'no img'
            bird['audio'] = 'no audio'
            bird['link'] = 'no link'
   
    return jsonify(birdsj)

@app.route('/regionData/<Region>')
def regionData(Region):
    regData = getRegionData.getRegionData(Region)
    top10 = getRegionData.getTop10(regData)
    return top10

@app.route('/birdRegData/<Region>')
def birdRegData(Region):
   regionData = getRegionData.getRegionData(Region)
   birds = getRegionData.getBirds(regionData)
   birdsj = eval(birds)

   results = session.query(Bird.Common_Name, Bird.Img_URL, Bird.Audio_URL, Bird.Info_URL)

   #Convert the query results to a Dictionary using date as the key and tobs as the value.
   data = {}

   # populate dict with rows from results
   for row in results:
       sp = str(row.Common_Name).lower()
       data[sp] = [row.Img_URL, row.Audio_URL, row.Info_URL]

   for bird in birdsj:
       sp = bird['comName'].lower()
       if sp in data.keys():
           bird['img'] = data[sp][0]
           bird['audio'] = data[sp][1]
           bird['link'] = data[sp][2]
       else:
           bird['img'] = 'no img'
           bird['audio'] = 'no audio'
           bird['link'] = 'no link'
 
   return jsonify(birdsj)

# Route that returns list of states
@app.route('/stateCentroid')
def stateCentroid():
    results = session.query(StateCentroids.state_abbr, StateCentroids.state, StateCentroids.center_lat, StateCentroids.center_lng, StateCentroids.zoom)
    data = {}

    # populate the dictionary
    for row in results:
        sp = str(row.state_abbr).upper()
        data[sp] = [row.state, row.center_lat, row.center_lng, row.zoom]

    return jsonify(data)

# Route that returns list of regions
@app.route('/regionCentroid')
def regionCentroid():
    results = session.query(RegionCentroids.Region, RegionCentroids.Lat, RegionCentroids.Lng, RegionCentroids.Zoom)
    data = {}

    # populate the dictionary
    for row in results:
        sp = str(row.Region).title()
        data[sp] = [row.Lat, row.Lng, row.Zoom]

    return jsonify(data)

@app.route('/speciesData/<species>/<days>')
def speciesData(species, days):
    speciesData = getSpeciesData.speciesData(species, days)
    
    return speciesData

@app.route('/birdDB')
def birdDBList():
    results = session.query(Bird.Species_Code, Bird.Common_Name)

    #Convert the query results to a Dictionary using date as the key and tobs as the value.
    data = []

    # populate dict with rows from results
    for row in results:
        spRecord = {'code': row.Species_Code, 'comName': row.Common_Name}
        data.append(spRecord)

    return jsonify(data)

@app.route('/birdDB/<spCode>')
def birdDBPrint(spCode):
    results = session.query(Bird.Species_Code, Bird.Common_Name, Bird.Img_URL, Bird.Audio_URL, Bird.Info_URL).filter(Bird.Species_Code==spCode)

    #Convert the query results to a Dictionary using date as the key and tobs as the value.
    data = []

    # populate dict with rows from results
    for row in results:
        spRecord = {'code': row.Species_Code, 'comName': row.Common_Name, 
        'img': row.Img_URL, 'audio': row.Audio_URL, 'link': row.Info_URL}
        data.append(spRecord)

    return jsonify(data)

# Route for uploading images for classification
@app.route('/classifier', methods=['GET', 'POST'])
def upload_file():
    data = {'success': False}
    if request.method == 'POST':
        if request.files.get('file'):
            file = request.files['file']
            image = file.read()
            image = Image.open(io.BytesIO(image))

            image = prepare_image(image)
            global graph
            with graph.as_default():
                preds = model.predict(image)
                results = decode_predictions(preds)
                data['predictions'].append(r)

            data['success'] = True
    return jsonify(data)
    render_template("birdClassifier.html")

#################################################
if __name__ == "__main__":
    app.run(debug=True)
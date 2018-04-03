#################################################
# import necessary libraries
#################################################
import pandas as pd
import os
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

from flask import Flask, render_template, redirect, jsonify, request, url_for, send_from_directory


from sqlalchemy import Column, Float, Integer, String
from sqlalchemy import and_, or_
from sqlalchemy import func

from werkzeug.utils import secure_filename

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

#################################################
# route that renders index.html template
UPLOAD_FOLDER = 'static/images/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload')
def upload_start():
    return render_template('photoUpload.html')

@app.route('/upload/classify', methods=['POST'])
def classify():

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        sfname = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(sfname)
        model_file = "model/bird_categories_graph.pb"
        label_file = "model/bird_categories_labels.txt"
        spTable = classify_bird_image(sfname, model_file, label_file)
        top_category = spTable['category'][0]
        top_pct = round((spTable['probability'][0]*100),0)

        return render_template('photoID.html', top_category = top_category, top_pct = top_pct, 
    img_file = f'/upload/classify/{filename}')
    
@app.route('/upload/classify/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

from bird_classifier import classify_bird_image
from bird_classifier import load_graph
from bird_classifier import read_tensor_from_image_file
from bird_classifier import load_labels

#################################################
if __name__ == "__main__":
    app.run(debug=True)
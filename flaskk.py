from flask import Flask, render_template, request
import joblib
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
dfcenter = pd.read_csv('dfcenter.csv')


app = Flask (__name__)

@app.route ('/', methods = ['POST', 'GET'])
def home():
    return render_template('home.html')


@app.route('/result', methods = ['POST', 'GET'])
def results():
    if request.method == "POST":
        input = request.form
        lat1 = float(input['lat'])
        long1 = float(input['long'])
        dfs = pd.DataFrame()
        reg = input['region']
        if input['rain'].lower() == 'yes':
            dfs['rain'] = [1]
            rains = 'raining'
        else: 
            dfs['rain'] = [0]
            rains = 'not raining'
        if input['weekend'].lower() == 'yes':
            dfs['weekend'] = [1]
            week = 'weekend'
        else: 
            dfs['weekend'] = [0]
            week = 'weekday'
        dfs['temp'] = [int(input['temp'])]
        dfs['transitscore'] = [float(input['transit'])]
        dfs['bikescore'] = [float(input['bike'])]
        dfs['d_reg'] = [np.sqrt(((dfcenter[dfcenter['region']==reg]['lat'] - lat1)**2) + ((dfcenter[dfcenter['region']==reg]['long'] - long1)**2))]
        dfs['walkscore'] = [float(input['walk'])]
        potensi = int(round(((10**(model.predict(dfs)))[0])*12))
        
    return render_template('results.html',potensi = potensi, lat=lat1, long = long1, rains = rains, week = week)
  
if __name__ == '__main__':
    model = joblib.load ('modelgbr') 
    app.run(debug = True, port = 2020)
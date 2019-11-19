import pandas as pd
import numpy as np
import re
from sklearn.pipeline import Pipeline
import pickle
from sklearn.ensemble import RandomForestRegressor
import datetime
import os
from opencage.geocoder import OpenCageGeocode
from sklearn import base
from flask import Flask, render_template, request, redirect, url_for

path =(os.getcwd())



class ColumnSelectTransformer(base.BaseEstimator, base.TransformerMixin):
    
    def __init__(self, col_names):
        self.col_names = col_names  
    
    def fit(self, X, y=None):
        
        return self
    
    def transform(self, X):
        return X[self.col_names].values



key = 'd49c6352494c4ea7b7188e21045edaf5'
geocoder = OpenCageGeocode(key)

RF_cost = pickle.load(open('./Pickled Models/Model_cost_pkl', 'rb'))
RF_time = pickle.load(open('./Pickled Models/Model_time_pkl', 'rb'))
full_pipeline = pickle.load(open('./Pickled Models/full_pipeline_pkl', 'rb'))

date = datetime.datetime.now()
#date.strftime("%B")



app = Flask(__name__)
app.info={}
def haversine_np(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    distance = 3958.8 * c
    return distance


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/DT', methods = ['POST', 'GET'])
def DT():
    if request.method == 'GET':
        return render_template('DT.html')
        

def return_pred(PU_A, DO_A, PU_T):
    date = datetime.datetime.now()

    input_list = dict()
    inp = []
    PU = geocoder.geocode(PU_A)
    DO = geocoder.geocode(DO_A)
    pu_lat = PU[0]['geometry']['lat']
    pu_lon = PU[0]['geometry']['lng']
    do_lat = DO[0]['geometry']['lat']
    do_lon = DO[0]['geometry']['lng']

    cat_features = ['Shared Trip Authorized','Year','Pickup Hour', 'Month','Day']

    num_features = ['Trip Miles', 'Trips Pooled',  'Pickup Dist from Downtown', 'Dropoff Dist from Downtown']
    
    Trip_Miles = haversine_np (pu_lon, pu_lat,do_lon, do_lat)
    input_list['Year'] = 2019
    input_list['Trip Miles'] = Trip_Miles
    input_list['Trips Pooled'] = 1
    input_list['Shared Trip Authorized'] = True
    input_list['Pickup Hour'] = int(re.split(':',PU_T)[0])
    input_list['Pickup Dist from Downtown'] = haversine_np(pu_lon, pu_lat, -87.6298,41.8781)
    input_list['Dropoff Dist from Downtown'] = haversine_np(do_lon, do_lon, -87.6298,41.8781)
    input_list['Month'] = date.strftime("%B")
    input_list['Day'] = date.strftime("%A")
     
    X_test = pd.DataFrame.from_dict([input_list])
    #X = pipeline.transform(X_test)
    
    cost = RF_cost.predict(X_test)
    time = RF_time.predict(X_test)
    return ('$' + str(np.round(cost[0],2)), str(np.round(time[0],0)) + ' Minutes')
  
@app.route('/PP', methods = ['POST', 'GET'])
def PP():
    if request.method == 'GET':
        return render_template('PP.html')
    else:
        app.info['Pickup_Add'] = request.form['PU_Address']
        app.info['Dropoff_Add'] = request.form['DO_Address']
        app.info['Pickup_Time'] = request.form['PU_Time']
        Pred_cost,Pred_Time = return_pred (app.info['Pickup_Add'], app.info['Dropoff_Add'],app.info['Pickup_Time'])
        return render_template('PPred.html', Pred_Cost = Pred_cost, Pred_Time= Pred_Time,PU_Ad = app.info['Pickup_Add'], DO_Ad =app.info['Dropoff_Add']  )
   
@app.route('/PPred', methods = ['POST','GET'])
def PPred(PU_add):
    if request.method == 'GET':
        
        return render_template('PPred.html')
        
if __name__ == '__main__':
  app.run(debug=True)
  
  

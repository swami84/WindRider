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

RF_cost = pickle.load(open('C:/Machine Learning/Pickled Models/Model_cost_pkl', 'rb'))
RF_time = pickle.load(open('C:/Machine Learning/Pickled Models/Model_time_pkl', 'rb'))
driver_zc = pickle.load(open('./Pickled Models/Driver_TP_pkl', 'rb'))

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


##@app.route('/DT', methods = ['POST', 'GET'])
##def DT():
##    if request.method == 'GET':
##        return render_template('DT.html')
##        
def return_tpy(zipcode):
    zc = geocoder.geocode(zipcode)
    dr_lat = zc[0]['geometry']['lat']
    dr_lon = zc[0]['geometry']['lng']
    res_dist = haversine_np(dr_lon, dr_lat, -87.6298,41.8781)
    
    
    mean_tpy = driver_zc.intercept_ + (driver_zc.coef_[0]*res_dist)
    return mean_tpy

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
    input_list['Trips Pooled'] = 0
    input_list['Shared Trip Authorized'] = False
    input_list['Pickup Hour'] = int(re.split(':',PU_T)[0])
    input_list['Pickup Dist from Downtown'] = haversine_np(pu_lon, pu_lat, -87.6298,41.8781)
    input_list['Dropoff Dist from Downtown'] = haversine_np(do_lon, do_lat, -87.6298,41.8781)
    input_list['Month'] = date.strftime("%B")
    input_list['Day'] = date.strftime("%A")
     
    X_test_ncp = pd.DataFrame.from_dict([input_list])
    input_list['Shared Trip Authorized'] = True
    input_list['Trips Pooled'] = 2
    X_test_cp = pd.DataFrame.from_dict([input_list])
    cost_cp = RF_cost.predict(X_test_cp)
    carpool_cost = '$' + str(np.round(cost_cp[0],2))
    
    cost_ncp = RF_cost.predict(X_test_ncp)
    single_cost = '$' + str(np.round(cost_ncp[0],2))
                                       
    time_ncp = RF_time.predict(X_test_ncp)
    single_time = str(np.round(time_ncp[0],0)) + ' Minutes'
                                  
    time_cp = RF_time.predict(X_test_cp)
    carpool_time = str(np.round(time_cp[0],0)) + ' Minutes'

                                       
    return (carpool_cost,single_cost,carpool_time ,single_time)
  
@app.route('/PP', methods = ['POST', 'GET'])
def PP():
    if request.method == 'GET':
        return render_template('PP.html')
    else:
        app.info['Pickup_Add'] = request.form['PU_Address']
        app.info['Dropoff_Add'] = request.form['DO_Address']
        app.info['Pickup_Time'] = request.form['PU_Time']
        Pred_cost_cp, Pred_cost_single,Pred_Time_cp, Pred_Time_single = return_pred (app.info['Pickup_Add'], app.info['Dropoff_Add'],app.info['Pickup_Time'])
        return render_template('PPred.html', Pred_cost_cp = Pred_cost_cp, Pred_cost_single =Pred_cost_single,
                               Pred_Time_cp = Pred_Time_cp, Pred_Time_single = Pred_Time_single,
                               PU_Ad = app.info['Pickup_Add'], DO_Ad =app.info['Dropoff_Add']  )
   
@app.route('/PPred', methods = ['POST','GET'])
def PPred(PU_add):
    if request.method == 'GET':
        
        return render_template('PPred.html')

@app.route('/DT', methods = ['POST', 'GET'])
def DT():
    if request.method == 'GET':
        return render_template('DT.html')
    else:
        app.info['Zipcode'] = str(request.form['res_zip'])
        
        tpy_est = return_tpy(app.info['Zipcode'])
        return render_template('DPred.html', tpy_est = tpy_est )


@app.route('/DPred', methods = ['POST','GET'])
def DPred():
    if request.method == 'GET':
        return render_template('DPred.html')
        
if __name__ == '__main__':
  app.run(debug=True)
  
  

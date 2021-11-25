from flask import Flask, redirect, url_for, request, render_template, jsonify
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import datetime

import requests
import random

import pickle5 as pickle
from sklearn.neural_network import MLPClassifier
import numpy as np
import pandas as pd
from sklearn import preprocessing

filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

app = Flask(__name__)


Users = {"U1" : ["q", 0], "U2" : ["q", 1], "U3" : ["q", 2], "U4" : ["q", 3], "U5" : ["q", 4], "U6" : ["q", 5],
		"U7" : ["q", 6], "U8" : ["q", 7], "U9" : ["q", 8], "U10" : ["q", 9], "U11" : ["q", 10], "U12" : ["q", 11] }

Location ={"L1" : 0, "L2" : 1, "L3" : 2, "L4" : 3}

# r = requests.get(url = "http://ec2-13-233-216-58.ap-south-1.compute.amazonaws.com:5050/api/d2")
# data = r.json()
# print(data)

def get_timestamp(t):
	if t in range(0, 7):
		return 0
	elif t in range(8, 16):
		return 1
	else:
		return 2



@app.route('/')
def index():
	return render_template('index.html')


@app.route('/devices', methods = ['GET', 'POST'])
def devices():
	if request.method == "POST":
		data = request.get_json()
		user_id = data['user_id']
		location = data['location']
		device_id = data['device']
		today = datetime.datetime.now()
		date_time = get_timestamp(int(today.strftime("%H")))
		# print(device_id, (device_id % 3), user_id, location, date_time)
		pd_data = pd.DataFrame([[device_id, device_id, device_id % 3, user_id, user_id, location, date_time]], columns = ["Device", "Sensor_location", "Sensor_time_stamp", "Subject_ name", "Subject_ID", "Subject_location", "time_of_access"])
		result = loaded_model.predict(pd_data)
		print(int(result[0]))
		return {"result":int(result[0])}
	return "hi"

if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    app.run(debug = True, host = "0.0.0.0")

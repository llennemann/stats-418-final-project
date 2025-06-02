# backend for my web app in Flask
import os
from flask import Flask, jsonify, request
from model import build_prophet_model, make_predictions, filter_dataset_by_station, load_data

import json


HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def flask_app():
    app = Flask(__name__)
    df = load_data()  # Load the data once at the start
    print(df['timestamp_conv'].dtype)

    @app.route('/', methods=['GET'])
    def server_is_up():
        # print("success")
        return 'backend running! :)   \n \n'


    # take station ID from user, # of hours or days to predict, and H OR D
    # return prediction from prophet model based on historical data
    @app.route('/forecast-traffic', methods=['POST'])
    def predict_station():
        # read in payload
        body = request.json
        station_id = int(body.get("station_id"))
        num_periods = int(body.get("periods"))
        freq = body.get("freq") # H for hourly, D for daily

        # filter based on user input of station ID
        print("Filtering dataset for station ID:", station_id, "...")
        filtered_df = filter_dataset_by_station(df, station_id)

        # build_prophet_model
        print("Building Prophet model...")
        mod = build_prophet_model(filtered_df)

        # predict
        print("Predicting...")
        make_predictions(mod, num_periods, freq)
        print("Prediction complete and plots created...")
        return jsonify({'message': 'Success'}), 200
    return app

if __name__ == '__main__':
    app = flask_app()
    app.run(debug=True, host='0.0.0.0',port=5001)
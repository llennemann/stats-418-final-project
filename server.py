# backend for my web app in Flask
import os
from flask import Flask, jsonify, request

import json


HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def flask_app():
    app = Flask(__name__)


    # define routes here....
    @app.route('/', methods=['GET'])
    def server_is_up():
        # print("success")
        return 'backend running! :)   \n \n'

    # @app.route('/power_of_two', methods=['POST'])
    # def start():
    #     to_predict = request.json

    #     print(to_predict)
    #     pred = predict(to_predict)
    #     return jsonify({"power of two":pred})
    return app

if __name__ == '__main__':
    app = flask_app()
    app.run(debug=True, host='0.0.0.0',port=5001)
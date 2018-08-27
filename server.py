# -*- coding: utf-8 -*-
# app.py
"""
 Using SQLAlchemy and Flask get db record.(GET)
"""
import os
from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from py.layout import application
# import ssl

app = Flask(__name__, template_folder='templates')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)
# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# context.load_cert_chain('cert.crt', 'server_secret.key')
# datasetpart = {}
# datasetparthourly = {}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def face_info():
    print(request.method)
    if request.method == "POST":
        # stream = request.get_data()
        data = application(request.data)
        if data == 'error':
            return 'error'
        else:
            return jsonify(data)


def write(array):
    post = Choice(array[0], array[1], array[2], array[3], array[4], array[5], array[6], array[7], array[8], array[9], array[10])
    print(post, array)
    db.session.add(post)
    db.session.commit()


class receive_json(Resource):
    def post(self):
        print('receive')
        json_data = request.get_json(silent=True, force=True)
        print(jsonify(json_data))

# api.add_resource(receive_json, '/upload')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    # app.run(debug=False, host='127.0.0.1', port=port)#, ssl_context=context, threaded=True)
    app.run(debug=False, host='0.0.0.0', port=port)

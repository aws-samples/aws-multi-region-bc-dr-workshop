#!/usr/bin/python
from __future__ import print_function
import os
import sys
import logging
import random
from urlparse import urlparse
from flask import Flask, jsonify, json, Response, request, abort
from flask_cors import CORS
import mysfitsTableClient

# Load functions/classes from aws xray sdk to instrument this service to trace incoming 
# http requests and downstream aws sdk calls. This includes the X-Ray Flask middleware
# [TODO] load x-ray recorder class
# [TODO] load x-ray patch function
# [TODO] load middleware function for flask


if 'LOGLEVEL' in os.environ:
    loglevel = os.environ['LOGLEVEL'].upper()
else:
    loglevel = 'ERROR'

logging.basicConfig(level=loglevel)

# Configure xray_recorder class to name your service and load the ECS plugin for 
# additional metadata.
# [TODO] configure the x-ray recorder with a service name and load the ecs plugin


# Configure X-Ray to trace service client calls to downstream AWS services
# [TODO] patch the boto3 library


app = Flask(__name__)
CORS(app)
app.logger

# Instantiate the Flask middleware
# [TODO] configure middleware with the flask app and x-ray recorder


# The service basepath has a short response just to ensure that healthchecks
# sent to the service root will receive a healthy response.
@app.route("/")
def health_check_response():
    return jsonify({"message" : "This is for health checking purposes."})

@app.route("/mysfits/<mysfit_id>/like", methods=['POST'])
def like_mysfit(mysfit_id):
    app.logger.info('Like received.')
    if os.environ['CHAOSMODE'] == "on":
        n = random.randint(1,100)
        if n < 30:
            app.logger.warn('WARN: simulated 500 activated')
            abort(500)
        elif n < 60:
            app.logger.warn('WARN: simulated 404 activated')
            abort(404)
        app.logger.warn('WARN: This thing should NOT be left on..')
    
    service_response = mysfitsTableClient.likeMysfit(mysfit_id)
    flask_response = Response(service_response)
    flask_response.headers["Content-Type"] = "application/json"
    return flask_response

# Run the service on the local server it has been deployed to
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

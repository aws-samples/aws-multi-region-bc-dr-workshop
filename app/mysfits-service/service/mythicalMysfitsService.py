from flask import Flask, jsonify, json, Response, request
from flask_cors import CORS
import mysfitsTableClient
import requests
import json
import os
import logging
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# logging
if 'LOGLEVEL' in os.environ:
    loglevel = os.environ['LOGLEVEL'].upper()
else:
    loglevel = 'ERROR'

logging.basicConfig(level=loglevel)

plugins = ('ecs_plugin',)
xray_recorder.configure(
  service = 'Mysfits Service',
  plugins = plugins,
  #daemon_address='172.17.0.2:2000', # for local testing
  context_missing='LOG_ERROR'
)

libraries = ('boto3',)
patch(libraries)

app = Flask(__name__)
CORS(app)
app.logger

XRayMiddleware(app, xray_recorder)

if (os.environ['AWS_REGION'] != ''):
    region = os.environ['AWS_REGION']
else:
    r = requests.get("http://169.254.169.254/latest/dynamic/instance-identity/document")
    region = r.json()['region']

# A very basic API created using Flask that has two possible routes for requests.

# The service basepath has a short response just to ensure that healthchecks
# sent to the service root will receive a healthy response.
@app.route("/")
def mainSite():
    http_response = '''
        <!DOCTYPE html>
        <html lang="en">
          <head>
            <title>Mythical Mysfits</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
            <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.5.6/angular.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js"></script>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css">
          </head>
          <body ng-app="mysfitsApp" style="background-color:#EBEBEB">
            <style>
              @media (max-width: 800px) {
              	img {
                  max-width: 300px;
              	}
              }
            </style>
            <br>
            <div>Current region: %s</div>
            <div style="text-align: center">
              <img src="https://www.mythicalmysfits.com/images/mysfits_banner.gif" width="800px" align="center">
            </div>
            <br>
            <div class="container">
              <div id="mysfitsGrid" class="row" ng-controller="mysfitsListController">
                  <div class="col-md-4 border border-warning" ng-repeat="mysfit in mysfits">
                      <br>
                      <p align="center">
                        <strong> {{mysfit.name}}</strong>
                        <br>
                        <img src="{{mysfit.thumbImageUri}}" alt="{{mysfit.Name}}">
                      </p>
                      <p>
                        <br>
                        <b>Species:</b> {{mysfit.species}}
                        <br>
                        <b>Age:</b> {{mysfit.age}}
                        <br>
                        <b>Good/Evil:</b> {{mysfit.goodevil}}
                        <br>
                        <b>Lawful/Chaotic:</b> {{mysfit.lawchaos}}
                        <span style="float:right;">
                          <img id="{{mysfit.mysfitId}}LikeIcon" ng-click="likeClicked(mysfit.mysfitId)" src="https://www.mythicalmysfits.com/images/like_icon_false.png" onmouseover="" style="cursor: pointer;">
                          <img id="{{mysfit.mysfitId}}AlreadyLikedIcon" class="d-none" src="https://www.mythicalmysfits.com/images/like_icon_true.png" >
                        </span>
                      </p>
                  </div>
                </div>
              </div>
            <p>
              <br>
              <br>
              &nbsp;&nbsp;This site was created for use in the AWS Modern Application Workshop. <a href="https://github.com/aws-samples/aws-modern-application-workshop">Please see details here.</a>
            </p>
          </body>
          <script>
                    
            //var mysfitsApiEndpoint = 'REPLACE_ME_API_ENDPOINT';
            //var mysfitsApiEndpoint = 'http://localhost:8080'

            var app = angular.module('mysfitsApp', []);
        
            var gridScope;
        
            var filterScope;
        
            app.controller('clearFilterController', function($scope) {
            });
        
            app.controller('mysfitsFilterController', function($scope) {
        
              filterScope = $scope;
        
              // The possible options for Mysfits to populate the dropdown filters.
              $scope.filterOptionsList =
               {
                 "categories": [
                   {
                     "title": "Good/Evil",
                     "selections":  [
                       "Good",
                       "Neutral",
                       "Evil"
                     ]
                   },
                   {
                     "title": "Lawful/Chaotic",
                     "selections":  [
                       "Lawful",
                       "Neutral",
                       "Chaotic"
                     ]
                   }
                 ]
               };
        
               $scope.removeFilter = function() {
                 allMysfits = getAllMysfits(applyGridScope);
               }
        
               $scope.queryMysfits = function(filterCategory, filterValue) {
        
                   var filterCategoryQS = "";
                   if (filterCategory==="Good/Evil") {
                     filterCategoryQS = "GoodEvil";
                   } else {
                     filterCategoryQS = "LawChaos"
                   }
                   var mysfitsApi = '/mysfits?' + 'filter=' + filterCategoryQS + "&value=" + filterValue;

                   $.ajax({
                     url : mysfitsApi,
                     type : 'GET',
                     success : function(response) {
                       applyGridScope(response.mysfits)
                     },
                     error : function(response) {
                       console.log("could not retrieve mysfits list.");
                     }
                   });
               }
        
        
        
            });
        
            app.controller('mysfitsListController', function($scope) {
        
              gridScope = $scope;
        
              getAllMysfits(applyGridScope);

              $scope.likeClicked = function(mysfitId) {
                console.log("clicked: " + mysfitId);
                likeMysfit(mysfitId, updateLikeIcons);
              }
        
            });
        
            function applyGridScope(mysfitsList) {
              gridScope.mysfits = mysfitsList;
              gridScope.$apply();
            }
        
            function getAllMysfits(callback) {
        
              var mysfitsApi = '/mysfits';
        
              $.ajax({
                url : mysfitsApi,
                type : 'GET',
                success : function(response) {
                  callback(response.mysfits);
                },
                error : function(response) {
                  console.log("could not retrieve mysfits list.");
                }
              });
            }

            function updateLikeIcons(mysfitId) {
              likeIconId = "#" + mysfitId + "LikeIcon";
              $(likeIconId).addClass("d-none");
              alreadyLikedIconId = "#" + mysfitId + "AlreadyLikedIcon";
              $(alreadyLikedIconId).removeClass("d-none");
            }
        
            function likeMysfit(mysfitId, callback) {
              try {
                var mysfitsApi = '/mysfits/' + mysfitId + "/like";
                //var mysfitsApi = 'http://localhost:8000/mysfits/' + mysfitId + "/like";
                var reqData = {
                  url : mysfitsApi,
                  type : 'POST',
                  success : function(response) {
                    console.log("here" + mysfitId);
                    callback(mysfitId);
                  },
                  error : function(response) {
                    console.log("could not like mysfit");
                    console.log(response);
                    if (response.status == "401") {
                      alert("You must be logged in to adopt a mysfit.");
                    }
                  }
                }
                
                $.ajax(reqData);
              } catch(err) {
                console.log(err.message);
              }
            }
        
          </script>
        </html>
        ''' % region 
    return http_response

# Returns the data for all of the Mysfits to be displayed on
# the website.  If no filter query string is provided, all mysfits are retrived
# and returned. If a querystring filter is provided, only those mysfits are queried.
@app.route("/mysfits")
def getMysfits():

    filterCategory = request.args.get('filter')
    if filterCategory:
        filterValue = request.args.get('value')
        queryParam = {
            'filter': filterCategory,
            'value': filterValue
        }
        # a filter query string was found, query only for those mysfits.
        serviceResponse = mysfitsTableClient.queryMysfits(queryParam)
    else:
        # no filter was found, retrieve all mysfits.
        app.logger.info('retrieving all mysfits')
        serviceResponse = mysfitsTableClient.getAllMysfits()

    flaskResponse = Response(serviceResponse)
    flaskResponse.headers["Content-Type"] = "application/json"

    return flaskResponse

# Run the service on the local server it has been deployed to,
# listening on port 8080.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

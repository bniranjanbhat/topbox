from bson import json_util, ObjectId
from flask import Flask,jsonify
from flask import request
import sys
from datetime import datetime
from app.parameter_error import ParameterError

from app.helpers import mongo_client

API_VERSION = '1.0'

app = Flask(__name__)
db = mongo_client()


@app.route('/')
def root():
    response = {'apiVersion': API_VERSION, 'appName': 'Topbox Backend Take Home Test'}
    return json_util.dumps(response)


@app.route('/clients')
def clients():
    return json_util.dumps(db.clients.find({}))


@app.route('/clients/<client_id>')
def clients_by_id(client_id):
    client_object_id = ObjectId(client_id)
    return json_util.dumps(db.clients.find_one({'_id': client_object_id}))


@app.route('/engagements')
def engagements():
    return json_util.dumps(db.engagements.find({}))



@app.route('/engagements/<engagement_id>')
def engagements_by_id(engagement_id):
    engagement_object_id = ObjectId(engagement_id)
    return json_util.dumps(db.engagements.find_one({'_id': engagement_object_id}))

@app.route('/interactions')
def interactions():
    return json_util.dumps(db.interactions.find({}))

@app.route('/interactions/<engagement_id>')
def interactions_by_engagement_id(engagement_id):
    query={}
    query['engagementId']=ObjectId(engagement_id)
    try:
        start_str = request.args.get('startDate', default = None, type = str)
        if start_str:
            start_date = datetime.strptime(start_str, '%Y-%m-%dT%H')
            query['interactionDate'] = {'$gte': start_date } 
    except ValueError as err:
       raise ParameterError(f'startDate parse error {err}', status_code=400)

    try:
        end_str = request.args.get('endDate', default = None, type = str)
        if end_str:
            end_date = datetime.strptime(end_str, '%Y-%m-%dT%H')
            if 'interactionDate' in query.keys():
                query['interactionDate']['$lt'] = end_date
            else:
                query['interactionDate'] = {'$lt': end_date }
    except ValueError as err:
       raise ParameterError(f'endDate parse error {err}', status_code=400)   
  
    return json_util.dumps(db.interactions.find(query))


@app.route('/interactions/<interaction_id>')
def interactions_by_id(interaction_id):
    interaction_object_id = ObjectId(interaction_id)
    return json_util.dumps(db.interactions.find_one({'_id': interaction_object_id}))


@app.errorhandler(ParameterError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
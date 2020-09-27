from flask_restful import Api, Resource, reqparse
from flask import Flask
import os
import logging
import threading
import json
from flask_cors import CORS, cross_origin
from centroid import Centroid
from dbscanner import DBScanner
import re, csv, sys, configparser

CONFIG = configparser.ConfigParser()
CONFIG.read('config')
DATA = 'data/cordenate.csv'

LOG_LEVEL = {"develop": logging.DEBUG,
             "test": logging.INFO,
             "production": logging.WARNING}

# environment = os.getenv('ENVIRONMENT')
environment = "develop"

logging.basicConfig(
    level=LOG_LEVEL[environment])

app = Flask(__name__)
api = Api(app)
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r'/*': {'origins': '*'}})

class Health(Resource):
    def get(self):
        status = {'status': 'up'}, 200
        logging.debug(status, extra={'site': 'SOCL'})
        return status

class Calcule(Resource):
    def get(self):
        status = {'calculated': 'yes'}, 200
        main()
        return status

def get_data(config):
    data = []
    with open(DATA, 'r') as file_obj:
        csv_reader = csv.reader(file_obj)
        for id_, row in enumerate(csv_reader):
            if len(row) < config['dim']:

                print ("ERROR: The data you have provided has fewer \
                    dimensions than expected (dim = %d < %d)"
                    % (config['dim'], len(row)))
                sys.exit()
            else:
                point = {'id':id_, 'value': []}
                for dim in range(0, config['dim']):
                    point['value'].append(float(row[dim]))
                data.append(point)
    print("data")
    print(data)
    return data

def read_config():
    try:
        config = {"eps":float(CONFIG['DEFAULT']['eps']), \
                    "min_pts":float(CONFIG['DEFAULT']['min_pts']),\
                    "dim" : int(CONFIG['DEFAULT']['dim']) }
    except:
        print ("Error reading the configuration file.\
            expected lines: param = value \n param = {eps, min_pts, dim}, \
            value = {float, int, int}")
        sys.exit()
    return config

def main():
    config = read_config()
    dbc = DBScanner(config)
    data = get_data(config)
    print('data')
    print(data)
    dbc.dbscan(data)
    dbc.export()

# Flask Endpoints Conf

parser = reqparse.RequestParser();
parser.add_argument('points', action='append')

config = read_config()
# Todo
# shows a single todo item and lets you delete a todo item
class Point(Resource):
    def post(self):
        args = parser.parse_args()
        data = {'points': args['points']}

        def jsonTransformLib(s):
            return json.loads(str(s).replace("'", '"'))
        def libTransformDbScan(s):
            return dict(id = int(s['nro_oc']), value = [float(s['lat']), float(s['lng'])])
        map_iterator = map(jsonTransformLib, data['points'])
        output_list = list(map_iterator)
        lib_iterator = map(libTransformDbScan, output_list)
        lib_list = list(lib_iterator)

        # print ("DBScanner")
        dbc = DBScanner(config)
        dbc.dbscan(lib_list)
        #dbc.export()
        # print ("getData")
        clusters = dbc.getData()
        centroid = Centroid(clusters)
        centroid.get_centroide()
        return clusters, 201

api.add_resource(Health, "/info/health")
api.add_resource(Calcule, "/calcule")
api.add_resource(Point, "/points")

if __name__ == "__main__":
    logging.info(' Main: Inicio app', extra={'site': ''})
    from waitress import serve
    print("Start app")
    serve(app, host="0.0.0.0", port=8080)

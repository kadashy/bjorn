from flask_restful import Api, Resource
from flask import Flask
import os
import logging
import threading

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
    dbc.dbscan(data)
    dbc.export()

api.add_resource(Health, "/info/health")
api.add_resource(Calcule, "/calcule")

if __name__ == "__main__":
    logging.info(' Main: Inicio app', extra={'site': ''})
    from waitress import serve
    print("Start app")
    serve(app, host="0.0.0.0", port=8080)

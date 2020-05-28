from flask import Flask
from flask import request
from flask import jsonify
import os
import os
import requests
from time import time
import json

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():
    data = request.files
    file_name = data.get("somefile").filename
    start = time()
    valid_feature_types = {
                        'Point': 0,
                        'LineString': 0,
                        'Polygon': 0,
                        'MultiPoint': 0,
                        'MultiLineString': 0,
                        'MultiPolygon': 0,
                        'GeometryCollection': 0
                        } 
    with open(file_name) as f:
        data = json.load(f)
        
        if 'type' not in data.keys() and data['type'] != 'FeatureCollection':
            return "Не корректная структкра файла!"
            
        if 'features' not in data.keys():
            return "Не корректная структкра файла!"
            
        feature_list = data['features']
        result = {}        
        for feature in feature_list:
            if 'geometry' not in feature.keys() and 'type' not in feature['geometry'].keys():
                return "Не корректная структкра файла!"
            
            feature_type = feature['geometry']['type']
            
            if feature_type == 'GeometryCollection':
                valid_feature_types['GeometryCollection'] = valid_feature_types['GeometryCollection'] + 1
                
                if 'geometries' not in feature['geometry'].keys():
                    return "Не корректная структкра файла!"
                
                sub_feature_types = feature['geometry']['geometries']
                
                for sub_feature in sub_feature_types:
                    if sub_feature['type'] in valid_feature_types.keys():
                        valid_feature_types[sub_feature['type']] = valid_feature_types[sub_feature['type']] + 1               
            
            elif feature_type in valid_feature_types.keys():
                valid_feature_types[feature_type] = valid_feature_types[feature_type] + 1            
            else:
                return "Не корректная структкра файла!"
        time_duration = time() - start
        print("calculate_time", time_duration)
    return jsonify(valid_feature_types)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1488, debug=True)
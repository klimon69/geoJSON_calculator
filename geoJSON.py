#source env/bin/activate
from flask import Flask, jsonify, request, redirect
import os
import json
from time import time

ALLOWED_EXTENSIONS = {'json'}

app = Flask(__name__)

       
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET','POST'])
def upload_file():
    start1 = time()
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            return calculate_types(file.filename)
    time_duration1 = time() - start1
    print("upload_time", time_duration1)
    return '''
    <!doctype html>
    <title>geoJSON service</title>
    <h1>Upload GeoJSON FeatureCollection file</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Convert">
    </form>
    '''

def calculate_types(filename):
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
    with open(filename) as f:
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
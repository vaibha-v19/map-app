from flask import Flask, jsonify, request
import csv
import math
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Load the CSV data from the file
ocean_data = []
with open('static/ocean_data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        ocean_data.append({
            'lat': float(row['Latitude']),
            'lng': float(row['Longitude']),
            'depth': float(row['Depth']),
            'salinity': float(row['Salinity']),
            'conductivity': float(row['Conductivity'])
        })

# Helper function to find the nearest point if an exact match isn't available
def get_nearest_point(lat, lng):
    nearest_point = None
    nearest_distance = float('inf')
    for point in ocean_data:
        distance = math.sqrt((point['lat'] - lat) ** 2 + (point['lng'] - lng) ** 2)
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_point = point
    return nearest_point

# API to fetch data based on coordinates
@app.route('/get-data')
def get_data():
    lat = float(request.args.get('lat'))
    lng = float(request.args.get('lng'))

    # Try to find the exact point
    for point in ocean_data:
        if point['lat'] == lat and point['lng'] == lng:
            return jsonify(point)

    # If exact point not found, find the nearest point
    nearest_point = get_nearest_point(lat, lng)
    return jsonify(nearest_point)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

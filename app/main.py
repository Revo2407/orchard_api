from flask import request, jsonify
import pandas as pd
import numpy as np
from scipy.spatial import ConvexHull, distance_matrix
from shapely.geometry import Point, Polygon
from datetime import datetime
from app import app
import requests
import os

# Load the API token from environment variables
auth_token = os.getenv('AERO_AUTH')


# Function to parse dates in different formats
def parse_date(date_str):
    for fmt in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%d'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date format not recognized for date: {date_str}")

# Function to find the latest survey ID
def get_latest_survey(orchard_id):
    url = f"https://api.aerobotics.com/farming/surveys/?orchard_id={orchard_id}&limit=100&offset=0"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    surveys = response.json().get('results', [])
    latest_survey = max(surveys, key=lambda x: parse_date(x['date']))
    return latest_survey['id']

# Function to retrieve orchard data based on survey ID
def get_orchard_data(survey_id):
    url = f"https://api.aerobotics.com/farming/surveys/{survey_id}/tree_surveys/"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    orchard_data = response.json().get('results', [])
    orchard_df = pd.DataFrame(orchard_data)
    return orchard_df

# Function to find missing tree centroids
def find_missing_tree_centroids(tree_data, grid_size=0.00002, group_threshold=0.00005, noise_threshold=0.00002):
    coordinates = tree_data[['lng', 'lat']].values
    hull = ConvexHull(coordinates)
    hull_points = coordinates[hull.vertices]
    hull_polygon = Polygon(hull_points)

    min_lng, max_lng = coordinates[:, 0].min(), coordinates[:, 0].max()
    min_lat, max_lat = coordinates[:, 1].min(), coordinates[:, 1].max()
    lng_grid = np.arange(min_lng, max_lng, grid_size)
    lat_grid = np.arange(min_lat, max_lat, grid_size)
    lng_grid, lat_grid = np.meshgrid(lng_grid, lat_grid)

    grid_points = np.vstack((lng_grid.ravel(), lat_grid.ravel())).T

    # Check which grid points are inside the boundary using Shapely
    inside_mask = np.array([hull_polygon.contains(Point(x, y)) for x, y in grid_points])
    inside_grid_points = grid_points[inside_mask]

    tree_positions = coordinates
    distances = distance_matrix(tree_positions, inside_grid_points)
    min_distances = distances.min(axis=0)
    no_tree_points = inside_grid_points[min_distances > group_threshold]

    missing_tree_distances = distance_matrix(no_tree_points, no_tree_points)
    centroids = []
    assigned = np.zeros(no_tree_points.shape[0], dtype=bool)

    for i in range(no_tree_points.shape[0]):
        if assigned[i]:
            continue
        nearby_indices = np.where(missing_tree_distances[i] < group_threshold)[0]
        if len(nearby_indices) > 1:
            centroid = no_tree_points[nearby_indices].mean(axis=0)
        else:
            centroid = no_tree_points[i]
        centroids.append(centroid)
        assigned[nearby_indices] = True

    centroids = np.array(centroids)
    centroid_distances = [hull_polygon.exterior.distance(Point(x, y)) for x, y in centroids]
    non_noise_centroids = centroids[np.array(centroid_distances) > noise_threshold]

    return non_noise_centroids

# Route to process data and find missing trees
@app.route('/orchards/<int:orchard_id>/missing-trees', methods=['GET'])
def get_missing_trees(orchard_id):
    try:
        survey_id = get_latest_survey(orchard_id)
        orchard_df = get_orchard_data(survey_id)

        # Call the function to find missing tree centroids
        missing_tree_centroids = find_missing_tree_centroids(orchard_df)
        missing_trees_list = [{"lat": lat, "lng": lng} for lng, lat in missing_tree_centroids]

        return jsonify({"missing_trees": missing_trees_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

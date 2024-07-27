from flask import Blueprint, jsonify
from .services.tree_analysis import find_missing_tree_centroids
from .services.api_client import fetch_latest_survey_data, fetch_tree_surveys
import pandas as pd

main = Blueprint('main', __name__)

@main.route('/orchards/<int:orchard_id>/missing-trees', methods=['GET'])
def get_missing_trees(orchard_id):
    # Fetch latest survey data
    survey_data = fetch_latest_survey_data(orchard_id)
    if 'error' in survey_data:
        return jsonify(survey_data), survey_data.get('status', 500)
    
    # Extracting the latest survey by date
    latest_survey = max(survey_data['results'], key=lambda x: x['date'])
    latest_survey_id = latest_survey['id']
    
    # Fetch tree surveys
    tree_surveys_data = fetch_tree_surveys(latest_survey_id)
    if 'error' in tree_surveys_data:
        return jsonify(tree_surveys_data), tree_surveys_data.get('status', 500)

    # Extract relevant data into a DataFrame
    df = pd.DataFrame(tree_surveys_data['results'])
    
    # Finding missing tree centroids
    missing_centroids = find_missing_tree_centroids(df)

    # Format the centroids as a list of dictionaries
    missing_trees = [{"lat": coord[1], "lng": coord[0]} for coord in missing_centroids]
    return jsonify({"missing_trees": missing_trees})

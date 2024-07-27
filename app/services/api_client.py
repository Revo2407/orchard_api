import requests
import os

auth_token = os.environ.get('AERO_AUTH')

def fetch_latest_survey_data(orchard_id):
    url = f"https://api.aerobotics.com/farming/surveys/?orchard_id={orchard_id}&limit=100&offset=0"
    headers = {"accept": "application/json", "Authorization": f"Bearer {auth_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to retrieve data", "status": response.status_code}
    return response.json()

def fetch_tree_surveys(survey_id):
    url = f"https://api.aerobotics.com/farming/surveys/{survey_id}/tree_surveys/?limit=100&offset=0"
    headers = {"accept": "application/json", "Authorization": f"Bearer {auth_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to retrieve tree survey data", "status": response.status_code}
    return response.json()

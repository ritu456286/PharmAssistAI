import requests
from utils.api.api_config import ALERT_ROUTES as BASE_URL


def get_all_alerts():
    url = f"{BASE_URL}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except requests.exceptions.RequestException as e:
        return []

def update_alert(medicine_id, threshold):
    try:
        response = requests.patch(f"{BASE_URL}/{medicine_id}", json={"new_threshold": threshold})
        return response.status_code == 200  
    except requests.exceptions.RequestException as e:   
        return False
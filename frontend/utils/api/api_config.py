from dotenv import load_dotenv
import os
load_dotenv()

MEDICINE_ROUTES = os.getenv("BASE_URL") + "api/medicines" # Adjust if running on a different port

ALERT_ROUTES = os.getenv("BASE_URL") + "api/alerts" # Adjust if running on a different port
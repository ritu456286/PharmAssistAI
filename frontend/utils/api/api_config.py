from dotenv import load_dotenv
import os
load_dotenv()

MEDICINE_ROUTES = os.getenv("BASE_URL") + "api/medicines" # Adjust if running on a different port

ALERT_ROUTES = os.getenv("BASE_URL") + "api/alerts" # Adjust if running on a different port

AGENT_ROUTES = os.getenv("BASE_URL") + "api/agent" # Adjust if running on a different port

OCR_ROUTES = os.getenv("BASE_URL") + "api/process-image" # Adjust if running on a different port

INVOICE_ROUTES = os.getenv("BASE_URL") + "api/invoice" # Adjust if running on a different port
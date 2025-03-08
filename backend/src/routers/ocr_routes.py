# import os
# import shutil
# import json
# from fastapi import APIRouter, HTTPException, UploadFile, File
# from src.services.ocr_service import extract_json

# router = APIRouter()

# UPLOAD_DIR = "./uploads"  # Directory to temporarily store uploaded images
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# @router.post("/")
# async def process_image(file: UploadFile = File(...)):
#     """
#     Endpoint to accept an image file from the frontend, save it, and process it with OCR.
#     """
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     try:
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         # Get the extracted data (which may include markdown formatting)
#         extracted_data = extract_json(file_path)
#         print("***EXTRACTED DATA***", extracted_data)

#         # If the extracted data is a string with markdown formatting, remove it.
#         if isinstance(extracted_data, str):
#             # Remove markdown code block markers if present
#             if extracted_data.startswith("```json") and extracted_data.endswith("```"):
#                 extracted_data = extracted_data[len("```json"): -3].strip()

#             # Parse the string to a JSON object
#             try:
#                 extracted_data = json.loads(extracted_data)
#             except json.JSONDecodeError as e:
#                 raise HTTPException(status_code=500, detail=f"Error parsing JSON: {str(e)}")
        
#         return extracted_data

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

#     finally:
#         # Remove the file after processing
#         if os.path.exists(file_path):
#             os.remove(file_path)

import os
import shutil
from fastapi import APIRouter, HTTPException, UploadFile, File
from src.services.ocr_service import extract_json  # Import the function

router = APIRouter()

UPLOAD_DIR = "./uploads"  # Temporary directory for uploaded images
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure the upload directory exists

@router.post("/")
async def process_image(file: UploadFile = File(...)):
    """
    API endpoint to accept an image file, process it with OCR, and return structured JSON data.
    """

    # Save the uploaded file temporarily
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Call the OCR function to extract JSON data
        extracted_data = extract_json(file_path)

        # Ensure response is a valid JSON dictionary
        if not isinstance(extracted_data, dict):
            raise ValueError("Extracted data is not a valid JSON object")

        print("*** EXTRACTED DATA ***", extracted_data)
        return extracted_data  # Return as JSON response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    finally:
        os.remove(file_path)  # Clean up the uploaded file after processing

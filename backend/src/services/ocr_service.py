import os
import json
from google import genai
from google.genai import types

def extract_json(image_path):
    """
    Processes an image of a doctor's prescription and extracts structured information in JSON format.

    Args:
        image_path (str): Path to the image file.

    Returns:
        dict: Extracted JSON data containing patient's name, prescribed medicines, doctor's name, clinic name, and date.
    """
    
    # Initialize the Gemini client
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    # Upload the image to Gemini API
    file = client.files.upload(file=image_path)

    model = "gemini-2.0-flash-exp"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=file.uri,
                    mime_type=file.mime_type,
                ),
            ],
        )
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="application/json",
        system_instruction=[
            types.Part.from_text(text="""Extract the following information from the provided doctor's handwritten prescription. If a field cannot be reliably extracted due to illegibility or absence, return `None` for that specific field. The output *must* be a valid JSON object.  

### Required Fields:  

- **\"Patient's Name\"**: Extract the patient's full name as a string.  
- **\"Medicines Prescribed\"**:  
  - Extract all possible medicine names from the prescription.  
  - Verify each extracted name to ensure it is an actual medication.  
  - If a name is not a real medicine, do not include it in the final list.  
  - If no valid medication names are found, return `None`.  
- **\"Doctor's Name\"**: Extract the doctor's full name as a string.  
- **\"Clinic Name\"**: Extract the clinic's name as a string.  
- **\"Date\"**: Extract the date of the prescription and format it as `YYYY-MM-DD`.  

### Validation and Extraction Guidelines:  

1. **Extract First, Verify Later**: Extract all potential medicine names before checking if they are real medications.  
2. **Medicine Name Validation**: After extraction, verify each name against real, commonly prescribed medications. Omit any name that is not a real medicine.  
3. **Multi-Word Medicine Names**: Ensure proper extraction of multi-word medication names (e.g., `\"Amoxicillin Clavulanate\"`).  
4. **Exclusion of Non-Medications**: Do not include dosages, frequencies, routes of administration (e.g., `\"10mg\"`, `\"BID\"`, `\"PO\"`), or other instructions.  
5. **Output Format**: The final output *must* be a JSON object containing *only* the fields listed above.  
6. **Return None**: If the list of medicines is empty after validation, return `None`.  
7. **Strict JSON**: Ensure the response strictly adheres to JSON formatting rules, without additional text or formatting elements such as backticks.  

### Example JSON Output:  

{
  \"Patient's Name\": \"John Doe\",
  \"Medicines Prescribed\": [\"Paracetamol\", \"Amoxicillin\", \"Ibuprofen\"],
  \"Doctor's Name\": \"Dr. Smith\",
  \"Clinic Name\": \"Sunrise Medical Clinic\",
  \"Date\": \"2024-03-08\"
}
"""),
        ],
    )

    # Stream the response from the model
    extracted_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        extracted_text += chunk.text

    # Ensure the output is a valid JSON object
    try:
        extracted_data = json.loads(extracted_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {str(e)}")

    return extracted_data

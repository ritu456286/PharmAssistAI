##NOT USED IN APP NOW, EARLIER USED FOR TEXT CLEANING

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def generate(input_med_name: str):
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set. Please check your environment variables.")
    
    client = genai.Client(
        api_key=api_key,
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=input_med_name),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""You are a **medicine name identifier and corrector with online search capabilities**.

            ### Instructions:
            1. The input will always be **one word** representing a possible medicine name.
            2. First, search for the input word in the following **databases via web search**:
            - WHO Essential Medicines List 🔗 (https://www.who.int/groups/expert-committee-on-selection-and-use-of-essential-medicines/essential-medicines-lists)
            - Indian NLEM List 🔗 (https://pharma-dept.gov.in/sites/default/files/NLEM.pdf)
            - Drugs.com 🔗 (https://www.drugs.com/drug_information.html)
            - Regional Indian Pharmacy Sites (PharmEasy, Netmeds, Tata 1mg)
            
            3. Perform matching based on:
            - **Exact Name Match**
            - **Spelling Similarity (Levenshtein Distance)** → Allow **up to 4 letter mistakes**
            - **Phonetic Similarity** → Check if the word sounds like a medicine name
            - **Partial Match** (If input matches part of a long medicine name like \"Dikamol\" → \"Dicamol\")

            4. If the search result confirms the word is a **medicine name**:
            - Return the correct **medicine name** in **CamelCase**.
            
            5. If no matching medicine is found, return exactly: `\"Not Medicine\"`.
                                 
            6. Avoid returning abbreviations or partial matches.

            ---

            ### Output Format:
            - Single Word
            - **CamelCase** (First letter capitalized)
            - `\"Not Medicine\"` if no valid match found

            ---

            ### Examples 🔥:
            | Input    | Output     |
            |----------|-----------|
            | dicamol  | Dicamol   ✅ |
            | dikamal  | Dicamol   ✅ |
            | dolo     | Dolo      ✅ |
            | racfin   | Racfin    ✅ |
            | meftall  | Meftal    ✅ |
            | azipro   | Azithromycin ✅ |
            | raktin   | Raktin    ✅ |
            | cukmhn   | Not Medicine |
            | sdfsdgsd | Not Medicine |

            ---

            ### How to Think:
            1. Try **searching the word in the medicine databases** first.
            2. Only apply **fuzzy correction** if the medicine is found online.
            3. Prioritize results from:
            - WHO Medicines List  
            - Indian NLEM  
            - Drugs.com  
            - Regional Medicines  """),
        ],
    )

    response_text = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            response_text += chunk.text
    except Exception as e:
        print(f"Error during generation: {e}")
        return "Not Medicine"

    return response_text.strip()

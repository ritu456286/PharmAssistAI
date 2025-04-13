# ##NOT USED IN APP NOW, EARLIER USED FOR TEXT CLEANING
# ## FUZZY + LLM based approach to extract medicines

# import spacy
# from spacy.matcher import Matcher
# from rapidfuzz import process, fuzz, utils
# from src.utils.gemini_med_corrector import generate
# from typing import Optional
# from fastapi import HTTPException

# VALID_MEDICINES = ["amoxicillin", "paracetamol", "ibuprofen", "cetirizine", "azithromycin", "omeprazole", "dolo", "rantac", "crocin"]

# nlp = spacy.load("en_ner_bc5cdr_md")


# def correct_medicine_llm(token: str) -> Optional[str]:
#     """
#     Corrects a medicine name using LLM.
#     Returns the corrected medicine name or None if LLM says it's not a medicine.
#     """
#     try:
#         print("***************CALLING LLM for *****" + token)
#         corrected = generate(token)
#         if corrected == "Not Medicine" or corrected == "Not" or len(corrected) <= 3 or corrected.lower() == token.lower(): #or corrected.lower() == token.lower(): #Added last condition to prevent returning same token
#             return None
#         print("***corrected***" + corrected)
#         return corrected
#     except Exception as e:
#         print(f"LLM Correction Error: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"LLM Correction Error: {str(e)}")
    

# def correct_medicine(med: str) -> Optional[str]:
#     """
#     Attempts to correct the medicine name using fuzzy matching against a list of valid medicines.
#     Falls back to LLM correction if no match is found.
#     """
#     print("*****RECIEVED MED*****  " + med)
#     best_match, score , _ = process.extractOne(med, VALID_MEDICINES, scorer=fuzz.WRatio, processor=utils.default_process)
#     if score >= 80:
#         print("****SPACY BEST MATCH**** " + best_match)
#         return best_match
#     return correct_medicine_llm(med)

# def is_likely_medicine(token) -> bool:
#     """
#     Heuristic to determine if a token is likely a medicine name.
#     """
#     return (
#         len(token.text) > 3  
#         and token.pos_ in ["NOUN", "X", "PROPN"]  # Minimum length
#         and any(char.isalpha() for char in token.text) # has letters
#         and not token.is_stop
#     )


# def extract_medicines(text):
#     doc = nlp(text)
#     medicines = set()

#     for ent in doc.ents:
#         if ent.label_ == "CHEMICAL":
#             medicines.add(ent.text.lower())

#     for token in doc:
#         token_text = token.text.strip().lower()
#         print("TOKEN: " + token_text)
#         if (
#             token_text not in medicines
#             and is_likely_medicine(token)     
#         ):
#             corrected_name = correct_medicine(token_text)
#             if corrected_name:
#                 medicines.add(corrected_name)

#     return list(medicines)

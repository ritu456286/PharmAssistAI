import spacy
from spacy.matcher import Matcher
from rapidfuzz import process, fuzz, utils
from src.utils.gemini_med_corrector import generate
from typing import Optional
from fastapi import HTTPException

VALID_MEDICINES = ["amoxicillin", "paracetamol", "ibuprofen", "cetirizine", "azithromycin", "omeprazole", "dolo", "rantac", "crocin"]

nlp = spacy.load("en_ner_bc5cdr_md")


def correct_medicine_llm(token: str) -> Optional[str]:
    """
    Corrects a medicine name using LLM.
    Returns the corrected medicine name or None if LLM says it's not a medicine.
    """
    try:
        print("***************CALLING LLM for *****" + token)
        corrected = generate(token)
        if corrected == "Not Medicine" or corrected == "Not" or len(corrected) <= 3 or corrected.lower() == token.lower(): #or corrected.lower() == token.lower(): #Added last condition to prevent returning same token
            return None
        print("***corrected***" + corrected)
        return corrected
    except Exception as e:
        print(f"LLM Correction Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"LLM Correction Error: {str(e)}")
    

def correct_medicine(med: str) -> Optional[str]:
    """
    Attempts to correct the medicine name using fuzzy matching against a list of valid medicines.
    Falls back to LLM correction if no match is found.
    """
    print("*****RECIEVED MED*****  " + med)
    best_match, score , _ = process.extractOne(med, VALID_MEDICINES, scorer=fuzz.WRatio, processor=utils.default_process)
    if score >= 80:
        print("****SPACY BEST MATCH**** " + best_match)
        return best_match
    return correct_medicine_llm(med)

def is_likely_medicine(token) -> bool:
    """
    Heuristic to determine if a token is likely a medicine name.
    """
    return (
        len(token.text) > 3  
        and token.pos_ in ["NOUN", "X", "PROPN"]  # Minimum length
        and any(char.isalpha() for char in token.text) # has letters
        and not token.is_stop
    )


def extract_medicines(text):
    doc = nlp(text)
    medicines = set()

    for ent in doc.ents:
        if ent.label_ == "CHEMICAL":
            medicines.add(ent.text.lower())

    for token in doc:
        token_text = token.text.strip().lower()
        print("TOKEN: " + token_text)
        if (
            token_text not in medicines
            and is_likely_medicine(token)     
        ):
            corrected_name = correct_medicine(token_text)
            if corrected_name:
                medicines.add(corrected_name)

    return list(medicines)


# def extract_medicines(doc):
#     """
#     Extracts medicines from the document using NER and POS-based methods with fuzzy matching.
#     Avoids duplicate corrections using a set to track already processed medicines.
#     """
#     medicines = []
#     ner_medicines_set = set()

#     # 1. NER-Based Extraction
#     for ent in doc.ents:
#         if ent.label_ == "CHEMICAL":
#             med_name = ent.text.strip().lower()
#             medicines.append((med_name, ent.start_char, ent.end_char))
#             ner_medicines_set.add(med_name)

#     # 2. POS-Based Extraction with Fuzzy Correction
#     for token in doc:
#         if token.pos_ in ["PROPN", "X"] and len(token.text) > 3:
#             token_text = token.text.strip()
#             if token_text.lower() not in ner_medicines_set:
#                 corrected = correct_medicine(token_text)
#                 if corrected:
#                     medicines.append((corrected, token.idx, token.idx + len(token.text)))
#                     ner_medicines_set.add(corrected.lower())
#     print("MEDICINES: " + medicines)
#     return medicines


# def extract_dosages(doc):
#     """
#     Extracts dosage amounts from the document using pattern matching for common dosage formats.
#     Returns a list of (dosage_text, start_position) tuples.
#     """
#     matcher = Matcher(nlp.vocab)
#     dosage_pattern = [
#         {"LIKE_NUM": True},
#         {"LOWER": {"IN": ["mg", "mcg", "ml", "g", "units", "tablets", "capsules"]}},
#     ]
#     matcher.add("DOSAGE", [dosage_pattern])
#     return [(doc[start:end].text, doc[start].idx) for match_id, start, end in matcher(doc)]


# def map_medicines_to_dosages(medicines, dosages, max_distance=30):
#     """
#     Maps medicines to their corresponding dosages based on proximity in the text.
#     Uses a two-pointer technique to optimize performance.
#     """
#     medicine_data = []
#     dosage_index = 0
#     num_dosages = len(dosages)

#     for med, start_pos, end_pos in medicines:
#         dosage = None
        
#         # Match the closest dosage using two pointers technique
#         while dosage_index < num_dosages:
#             dosage_text, dosage_pos = dosages[dosage_index]
#             distance = dosage_pos - end_pos

#             if 0 < distance <= max_distance:
#                 dosage = dosage_text
#                 dosage_index += 1  # Move dosage pointer ahead once matched
#                 break
#             elif distance > max_distance:
#                 break  # Stop loop because further dosages will be too far

#             dosage_index += 1  # If dosage is behind, skip to next dosage
#         if med:
#             medicine_data.append({"name": med, "dosage": dosage})

#     return medicine_data


# def extract_medicines_and_dosages(text):
#     """
#     Orchestrates the entire extraction pipeline.
#     Extracts medicines, dosages, and maps them together into a final structured list.
#     """
#     doc = nlp(text)
#     medicines = extract_medicines(doc)
#     dosages = extract_dosages(doc)
#     return map_medicines_to_dosages(medicines, dosages)



# # Function to extract medicines & dosages
# def extract_medicines_and_dosages(text):
#     doc = nlp(text)
#     medicines = []
#     # ner_medicines_set = set()
#     # 1. NER-Based Extraction
#     medicines = [ent.text.lower() for ent in doc.ents if ent.label_ == "CHEMICAL"]

#     # for ent in doc.ents:
#     #     if ent.label_ == "CHEMICAL":
#     #         medicines.append(ent.text.lower())
#     #         ner_medicines_set.add(ent.text.lower())

#     # # 2. POS-Based Extraction
#     # for token in doc:
#     #     if token.pos_ in ["PROPN", "X"] and len(token.text) > 3:
#     #         token_text = token.text.strip()
#     #         if token_text.lower() not in ner_medicines_set:
#     #             corrected = correct_medicine(token_text)
#     #             if corrected:
#     #                 medicines.append(corrected)
#     #                 ner_medicines_set.add(corrected.lower()) 

#     # Define a pattern to match dosages
#     matcher = Matcher(nlp.vocab)
#     dosage_pattern = [
#         {"LIKE_NUM": True},  # Match numbers (e.g., 500mg)
#         {"LOWER": {"IN": ["mg", "mcg", "ml", "g", "units", "tablets", "capsules"]}},  # Common dosage units
#     ]
#     matcher.add("DOSAGE", [dosage_pattern])

#     # Extract dosage amounts
#     dosages = [doc[start:end].text for match_id, start, end in matcher(doc)]
#      # Extract dosages with their token index
#     # dosages = [(doc[start:end].text, start) for match_id, start, end in matcher(doc)]
    
#     # Create medicine list with corresponding dosages
#     medicine_data = []
    
#     dosage_index = 0

#     for med in medicines:
#         dosage = None

#         # Assign the next dosage if it comes after the medicine name in the text
#         if dosage_index < len(dosages):
#             med_pos = doc.text.find(med)
#             dosage_pos = doc.text.find(dosages[dosage_index])

#             if dosage_pos > med_pos:
#                 dosage = dosages[dosage_index]
#                 dosage_index += 1
        
#         medicine_data.append({"name": med, "dosage": dosage})
#     return medicine_data
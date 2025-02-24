import spacy
nlp = spacy.load("en_ner_bc5cdr_md")


from spacy.matcher import Matcher

# Function to extract medicines & dosages
def extract_medicines_and_dosages(text):
    doc = nlp(text)
    
    # Extract medicines (chemical entities)
    medicines = [ent.text for ent in doc.ents if ent.label_ == "CHEMICAL"]

    # Define a pattern to match dosages
    matcher = Matcher(nlp.vocab)
    dosage_pattern = [
        {"LIKE_NUM": True},  # Match numbers (e.g., 500)
        {"LOWER": {"IN": ["mg", "mcg", "ml", "g", "units", "tablets", "capsules"]}},  # Common dosage units
    ]
    matcher.add("DOSAGE", [dosage_pattern])

    # Extract dosage amounts
    dosages = [doc[start:end].text for match_id, start, end in matcher(doc)]
    print(medicines, dosages)
    return medicines, dosages
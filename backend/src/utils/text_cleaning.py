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
        {"LIKE_NUM": True},  # Match numbers (e.g., 500mg)
        {"LOWER": {"IN": ["mg", "mcg", "ml", "g", "units", "tablets", "capsules"]}},  # Common dosage units
    ]
    matcher.add("DOSAGE", [dosage_pattern])

    # Extract dosage amounts
    dosages = [doc[start:end].text for match_id, start, end in matcher(doc)]
    
    # Create medicine list with corresponding dosages
    medicine_data = []
    
    dosage_index = 0

    for med in medicines:
        dosage = None

        # Assign the next dosage if it comes after the medicine name in the text
        if dosage_index < len(dosages):
            med_pos = doc.text.find(med)
            dosage_pos = doc.text.find(dosages[dosage_index])

            if dosage_pos > med_pos:
                dosage = dosages[dosage_index]
                dosage_index += 1
        
        medicine_data.append({"name": med, "dosage": dosage})

    return medicine_data
import pandas as pd
import spacy

# Load the dataset with transcripts
df = pd.read_csv("tsmc_earnings_calls_filtered.csv")

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Fill missing transcripts with empty strings
df["transcript"] = df["transcript"].fillna("")


# Apply NER to extract named entities from each transcript
def extract_entities(index, text):
    print(f"Processing row {index}...")
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]


# Create a new column with extracted entities
df["transcript_entities"] = [
    extract_entities(i, row) for i, row in enumerate(df["transcript"])
]

# Save this enhanced version
ner_output_path = "tsmc_earnings_calls_transcript_ner.csv"
df.to_csv(ner_output_path, index=False)

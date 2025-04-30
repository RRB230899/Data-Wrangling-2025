import pandas as pd
import spacy


def apply_ner(input_csv, output_csv):
    # Load spaCy English model
    nlp = spacy.load("en_core_web_sm")

    # Load input CSV
    df = pd.read_csv(input_csv)

    # Fill missing titles or snippets with blank strings
    df['title'] = df['title'].fillna('')
    df['snippet'] = df['snippet'].fillna('')

    # Define function to extract named entities
    def extract_entities(text):
        doc = nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]

    # Apply NER on title and snippet
    df['title_entities'] = df['title'].apply(extract_entities)
    df['snippet_entities'] = df['snippet'].apply(extract_entities)

    # Save the enhanced dataframe
    df.to_csv(output_csv, index=False)
    print(f"NER applied and saved to {output_csv}.")


if __name__ == "__main__":
    apply_ner('tsmc_server_earthquake_scrape_full_fixed_final.csv', 'tsmc_server_earthquake_with_ner.csv')

import pandas as pd
import spacy


def apply_ner(input_csv, output_csv):
    nlp = spacy.load("en_core_web_sm")
    df = pd.read_csv(input_csv)

    df['title'] = df['title'].fillna('')
    df['snippet'] = df['snippet'].fillna('')

    def extract_entities(text):
        doc = nlp(text)
        ents = [(ent.text, ent.label_) for ent in doc.ents]

        # Add manual keywords if they appear
        text_lower = text.lower()
        if 'earthquake' in text_lower:
            ents.append(('earthquake', 'EVENT'))
        if 'magnitude' in text_lower:
            ents.append(('magnitude', 'QUANTITY'))

        return ents

    df['title_entities'] = df['title'].apply(extract_entities)
    df['snippet_entities'] = df['snippet'].apply(extract_entities)

    df.to_csv(output_csv, index=False)
    print(f"NER with custom keywords applied and saved to {output_csv}.")


if __name__ == "__main__":
    apply_ner('tsmc_server_earthquake_scrape_full_fixed_final.csv', 'tsmc_server_earthquake_with_ner.csv')

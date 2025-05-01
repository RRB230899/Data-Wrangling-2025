import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import ast

# Load NER-enhanced news article data
ner_df = pd.read_csv("./../tsmc_server_earthquake_with_ner.csv")

# Convert stringified entity lists to actual lists
ner_df['title_entities'] = ner_df['title_entities'].apply(ast.literal_eval)
ner_df['snippet_entities'] = ner_df['snippet_entities'].apply(ast.literal_eval)

# Flatten all named entities into a single list
all_entities = []


def collect_entities(entities, text_source):
    # Always lowercase the source text for keyword search
    text_lower = text_source.lower()

    # Extract standard labels
    all_entities.extend([ent for ent, label in entities if label in {"ORG", "GPE", "PRODUCT", "MONEY", "DATE", "CARDINAL"}])

    # Add manually if present
    if 'earthquake' in text_lower:
        all_entities.append('earthquake')
    if 'magnitude' in text_lower:
        all_entities.append('magnitude')


# Apply for both title and snippet
for i in range(len(ner_df)):
    collect_entities(ner_df.loc[i, 'title_entities'], ner_df.loc[i, 'title'])
    collect_entities(ner_df.loc[i, 'snippet_entities'], ner_df.loc[i, 'snippet'])

# Count frequencies
entity_freq = Counter(all_entities)

# Generate word cloud
wordcloud = WordCloud(width=1000, height=600, background_color='white', colormap='viridis').generate_from_frequencies(entity_freq)

# Plot
plt.figure(figsize=(14, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Named Entities in TSMC Earthquake News (+ Keywords: Earthquake, Magnitude, Cardinal)", fontsize=16)
plt.tight_layout()
plt.show()

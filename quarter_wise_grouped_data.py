import pandas as pd
import matplotlib.pyplot as plt
import ast
from collections import Counter, defaultdict

# Load the dataset
df = pd.read_csv("tsmc_earnings_calls_transcript_ner.csv")

# Drop rows where 'q' or 'question' or 'transcript_entities' is missing
df = df.dropna(subset=["q", "question", "transcript_entities"])

# Convert transcript_entities from string to list of tuples
df["transcript_entities"] = df["transcript_entities"].apply(ast.literal_eval)

# Keep only quarters from Q1 2020 onwards
df = df[df["q"] >= "2020Q1"]

# Define important entity names to include in the plot
important_entities = {
    "Apple", "CapEx", "N3", "N5", "inventory", "IoT", "advanced",
    "5g era", "money", "AI", "technology", "USD", "smartphone", "N4P", "GPE"
}


# Function to flag important questions based on NER labels
def is_important_question(ner_list):
    important_labels = {"MONEY", "PERCENT", "ORDINAL", "CARDINAL", "ORG", "PRODUCT"}
    return any(ent[1] in important_labels for ent in ner_list)


# Add a flag for important questions
df["important_q_flag"] = df["transcript_entities"].apply(is_important_question)

# Group and count important entities per quarter
entity_counts_by_quarter = defaultdict(Counter)

for _, row in df.iterrows():
    quarter = row["q"]
    for entity, label in row["transcript_entities"]:
        if entity in important_entities:
            entity_counts_by_quarter[quarter][entity] += 1

# Convert to DataFrame
entity_plot_data = pd.DataFrame(entity_counts_by_quarter).T.fillna(0)

# Sort the DataFrame by quarter
entity_plot_data = entity_plot_data.sort_index()

# Plotting
plt.figure(figsize=(15, 8))
entity_plot_data.plot(kind='bar', stacked=True, figsize=(15, 8), colormap='tab20')
plt.title("Top Selected Named Entities per Quarter (2020Q1–2022Q2)", fontsize=16)
plt.xlabel("Quarter", fontsize=14)
plt.ylabel("Mention Frequency", fontsize=14)
plt.xticks(rotation=45)
plt.legend(title="Entity", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

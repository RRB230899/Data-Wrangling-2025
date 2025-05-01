import pandas as pd
import matplotlib.pyplot as plt

# === Load Data ===
stock_df = pd.read_csv("tsmc_quarterly_stock_prices.csv")
ner_df = pd.read_excel("NER_Filtered.xlsx")
quake_df = pd.read_csv("taiwan_earthquake_data_2020_to_2025.csv")
grouped_df = pd.read_csv("grouped_data.csv")

# === Preprocess NER Data ===
ner_df["combined_entities"] = (
    ner_df["title_entities"].astype(str) + ", " + ner_df["snippet_entities"].astype(str)
)
ner_df["combined_entities"] = ner_df["combined_entities"].apply(
    lambda x: ", ".join(sorted(set(x.split(", "))))
)
ner_summary = ner_df.groupby("q")["combined_entities"].apply(
    lambda x: ", ".join(sorted(set(x)))
).reset_index()
ner_summary.columns = ["q", "NER_Entities"]

# === Filter Earthquake Data (magnitude > 5.5) and Summarize ===
quake_df = quake_df[quake_df["magnitude"] > 5.5]
quake_summary = quake_df.groupby("q")["magnitude"].apply(
    lambda x: ", ".join(f"M{m:.1f}" for m in sorted(x))
).reset_index()
quake_summary.columns = ["q", "Earthquake_Mags"]

# === Merge All DataFrames ===
combined_df = stock_df.merge(grouped_df, on="q", how="left")
combined_df = combined_df.merge(ner_summary, on="q", how="left")
combined_df = combined_df.merge(quake_summary, on="q", how="left")

# === Compute % Change in Stock Price ===
combined_df = combined_df.sort_values("q")
combined_df["% Change"] = combined_df["Close"].pct_change().fillna(0) * 100


# === Annotate Each Bar ===
def build_annotation(row):
    annotations = []
    for col in grouped_df.columns:
        if col != "q" and pd.notna(row[col]) and row[col] > 0:
            annotations.append(f"{col}: {int(row[col])}")
    if pd.notna(row["NER_Entities"]):
        annotations.append("NERs: " + row["NER_Entities"])
    if pd.notna(row["Earthquake_Mags"]):
        annotations.append("Quake: " + row["Earthquake_Mags"])
    return "\n".join(annotations)


combined_df["Annotation"] = combined_df.apply(build_annotation, axis=1)


def custom_annotation(row):
    if row["q"] == "2025-Q1":
        return "dipped {:.1f}%\nCall: N5 Mass Production\nQuake: Mag 6.4" \
               "\nEarthquake may have affected 20,000 TSMC wafers".format(row["% Change"])
    else:
        trend_label = f"rose {abs(row['% Change']):.1f}%" if row["% Change"] >= 0 else f"dipped {abs(row['% Change']):.1f}%"
        parts = []
        for col in grouped_df.columns:
            if col != "q" and pd.notna(row[col]) and row[col] > 0:
                parts.append(f"{col}: {int(row[col])}")
        if pd.notna(row["NER_Entities"]):
            parts.append("NERs: " + row["NER_Entities"])
        if pd.notna(row["Earthquake_Mags"]):
            parts.append("Quake: " + row["Earthquake_Mags"])
        return f"{trend_label}\n" + "\n".join(parts)


# Apply the custom annotation
combined_df["Annotation"] = combined_df.apply(custom_annotation, axis=1)

# Re-plot with this new annotation
fig, ax = plt.subplots(figsize=(18, 8))
bars = ax.bar(combined_df["q"], combined_df["% Change"], color="cornflowerblue")

for bar, annotation in zip(bars, combined_df["Annotation"]):
    height = bar.get_height()
    if annotation.strip():
        ax.annotate(annotation,
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5 if height >= 0 else -15),
                    textcoords="offset points",
                    ha='center', va='bottom' if height >= 0 else 'top',
                    fontsize=8, rotation=90, color="darkred")

# Aesthetics
ax.axhline(0, color='black', linewidth=0.8)
ax.set_title("TSMC Quarterly Stock % Change Annotated with Earnings Call & Earthquake Events", fontsize=16)
ax.set_ylabel("% Change in Stock Price")
ax.set_xlabel("Quarter")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.show()
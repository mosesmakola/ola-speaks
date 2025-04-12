import pandas as pd
import json

# Load JSON
with open("bible_raw_data.json") as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

# Drop duplicates by book/chapter/verse
deduped_df = df.drop_duplicates(subset=["book", "chapter", "verse"])

print("Original:", len(df))
print("Unique:", len(deduped_df))
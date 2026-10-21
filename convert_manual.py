import pandas as pd
import re

# Read your newly uploaded Google Sheets export
df = pd.read_excel('US Congress.xlsx', sheet_name=0)

# 1. Rename Religious_1 or Religious Terms to Religious_Terms if needed
if 'Religious_1' in df.columns:
    df = df.rename(columns={'Religious_1': 'Religious_Terms'})

# 2. Clean up column names and whitespace
df.columns = [str(c).strip() for c in df.columns]

def clean_val(val):
    if isinstance(val, str):
        # Remove control characters and trim spaces
        val = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', '', val)
        return val.strip()
    return val

for col in df.columns:
    df[col] = df[col].apply(clean_val)

# Fix religion casing/duplicates
if 'Religious_Terms' in df.columns:
    df['Religious_Terms'] = df['Religious_Terms'].replace({'Lds': 'LDS', '': 'NOT LISTED'})

# Fill empty fields
df = df.fillna('NOT LISTED')

# Save directly to data.json
df.to_json('data.json', orient='records', indent=2)
print("Successfully converted Google Sheets data to data.json!")

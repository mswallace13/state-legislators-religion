import pandas as pd
import re

# Load dataset
df = pd.read_excel('US Congress (2).xlsx', sheet_name=0)

def clean_text(val):
    if isinstance(val, str):
        # Strip non-printable control characters
        val = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', '', val)
        return val.strip()
    return val

# Clean all string columns
for col in df.columns:
    df[col] = df[col].apply(clean_text)

# Clean Religious_Terms specifically
df['Religious_Terms'] = df['Religious_Terms'].replace({'Lds': 'LDS', 'LDS ': 'LDS'})

# Re-export clean data.json
df.fillna('NOT LISTED').to_json('data.json', orient='records', indent=2)
print("Successfully cleaned trailing spaces and case variations in data.json!")

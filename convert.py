import pandas as pd

# Read main sheet
df = pd.read_excel('US Congress (1).xlsx', sheet_name=0)
df = df.fillna('')

# Save JSON
df.to_json('data.json', orient='records', indent=2)
print("Successfully created data.json!")

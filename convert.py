import pandas as pd

# Read the newly uploaded US Congress (2).xlsx file
df = pd.read_excel('US Congress (2).xlsx', sheet_name=0)

# Replace missing/empty values with an empty string
df = df.fillna('')

# Save to data.json
df.to_json('data.json', orient='records', indent=2)
print("Successfully generated data.json from US Congress (2).xlsx!")

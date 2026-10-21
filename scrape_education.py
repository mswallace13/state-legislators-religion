import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Load dataset
df = pd.read_excel('US Congress (2).xlsx', sheet_name=0)

def clean_text(val):
    if isinstance(val, str):
        # Remove non-printable control characters
        val = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', '', val)
        return val.strip()
    return val

# Standardize religion strings (removes duplicates, trailing spaces, casing)
if 'Religious_Terms' in df.columns:
    df['Religious_Terms'] = df['Religious_Terms'].apply(clean_text)
    df['Religious_Terms'] = df['Religious_Terms'].replace({
        'Lds': 'LDS', 
        'LDS ': 'LDS',
        '': 'NOT LISTED'
    })

DEGREE_PATTERN = re.compile(
    r'\b(?:B\.?A\.?|B\.?S\.?|M\.?A\.?|M\.?S\.?|J\.?D\.?|Ph\.?D\.?|M\.?B\.?A\.?|Bachelor|Master|Doctorate|Juris Doctor)\b'
    r'[^.\n,;]*?(?:University|College|School|Institute|State|Academy|Law School)[^.\n,;]*',
    re.IGNORECASE
)

COLLEGE_PATTERN = re.compile(
    r'\b(?:University of [A-Z][a-z]+|[A-Z][a-z]+ State University|[A-Z][a-z]+ College|[A-Z][a-z]+ Law School)\b'
)

def extract_education(url):
    if not isinstance(url, str) or not url.startswith('http'):
        return 'NOT LISTED'
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code != 200:
            return 'NOT LISTED'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ')
        
        matches = DEGREE_PATTERN.findall(text)
        if not matches:
            matches = COLLEGE_PATTERN.findall(text)
        
        if matches:
            cleaned = list(set([clean_text(m.strip()) for m in matches if len(m.strip()) > 8]))
            if cleaned:
                return ' | '.join(cleaned[:2])
    except Exception:
        pass
    return 'NOT LISTED'

print("Scraping education details and cleaning religious terms...")
urls = df['Bio_URL'].tolist()

with ThreadPoolExecutor(max_workers=25) as executor:
    results = list(tqdm(executor.map(extract_education, urls), total=len(urls)))

df['Education'] = results

# Clean all string columns in dataframe
for col in df.columns:
    df[col] = df[col].apply(clean_text)

# Save to data.json and updated Excel file
df.fillna('NOT LISTED').to_json('data.json', orient='records', indent=2)
df.to_excel('US_Congress_Updated.xlsx', index=False)
print("Done! Cleaned dataset saved to data.json and US_Congress_Updated.xlsx.")

import json
import pandas as pd
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_FILE = DATA_DIR / "clean_majors.csv"
OUTPUT_FILE = DATA_DIR / "embeddings.json"

load_dotenv(BASE_DIR / ".env", override=False)
load_dotenv(BASE_DIR.parent / ".env", override=False)
client = OpenAI()

df = pd.read_csv(INPUT_FILE, dtype=str)

if OUTPUT_FILE.exists():
    embeddings = json.loads(OUTPUT_FILE.read_text())
else:
    embeddings = {}

total = len(df)
for idx, row in df.iterrows():
    code = str(row["CIPCode"])
    if code in embeddings:
        print(f"[{idx+1}/{total}] skip {code}")
        continue

    text = f"{row['CIPTitle']}\n\n{row['CIPDefinition']}"
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    embeddings[code] = response.data[0].embedding

    OUTPUT_FILE.write_text(json.dumps(embeddings))
    print(f"[{idx+1}/{total}] embedded {code}")

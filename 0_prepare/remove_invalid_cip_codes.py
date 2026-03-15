"""Remove invalid and catch-all CIP codes from clean data and embeddings.

This script removes CIP entries that are explicitly marked as invalid for IPEDS
or are catch-all ", Other" programs, then updates:
- data/clean_majors.csv
- data/embeddings.json

It also writes a report of removed codes to:
- data/results/data_quality/removed_invalid_cip_codes.csv
"""

import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CLEAN_MAJORS_FILE = DATA_DIR / "clean_majors.csv"
EMBEDDINGS_FILE = DATA_DIR / "embeddings.json"
REPORT_DIR = DATA_DIR / "results" / "data_quality"
REPORT_FILE = REPORT_DIR / "removed_invalid_cip_codes.csv"


def invalid_mask(df: pd.DataFrame) -> pd.Series:
    """Return rows that should be excluded from analysis outputs.

    Excludes:
    - CIP rows explicitly reserved / invalid for IPEDS
    - Catch-all programs labeled as ", Other"
    """
    title = df["CIPTitle"].fillna("")
    definition = df["CIPDefinition"].fillna("")
    return (
        title.str.fullmatch(r"Reserved\.", case=False)
        | definition.str.contains("Reserved for use by Statistics Canada", case=False)
        | definition.str.contains("not valid for IPEDS reporting", case=False)
        | title.str.contains(r",\s*Other\.?$", case=False, regex=True)
    )


def main() -> None:
    df = pd.read_csv(CLEAN_MAJORS_FILE, dtype=str)
    embeddings = json.loads(EMBEDDINGS_FILE.read_text())

    before_rows = len(df)
    before_embeddings = len(embeddings)

    mask = invalid_mask(df)
    removed = df.loc[mask, ["CIPCode", "CIPArea", "CIPTitle", "CIPDefinition"]].copy()
    removed = removed.sort_values("CIPCode").reset_index(drop=True)
    removed_codes = set(removed["CIPCode"].tolist())

    cleaned_df = df.loc[~mask].copy().reset_index(drop=True)
    cleaned_embeddings = {
        code: vec for code, vec in embeddings.items() if code not in removed_codes
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    removed.to_csv(REPORT_FILE, index=False)
    cleaned_df.to_csv(CLEAN_MAJORS_FILE, index=False)
    EMBEDDINGS_FILE.write_text(json.dumps(cleaned_embeddings))

    print(f"Removed CIP codes: {len(removed_codes)}")
    if removed_codes:
        print("Codes:", ", ".join(sorted(removed_codes)))
    print(f"clean_majors rows: {before_rows} -> {len(cleaned_df)}")
    print(f"embeddings count:  {before_embeddings} -> {len(cleaned_embeddings)}")
    print(f"Removal report:    {REPORT_FILE}")


if __name__ == "__main__":
    main()

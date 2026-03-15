import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_FILE = DATA_DIR / "CIPCode2020.csv"
OUTPUT_FILE = DATA_DIR / "clean_majors.csv"

# Expanded set: original top-12 plus additional high-coverage areas.
SELECTED_AREAS = {
    "01", "05", "09", "11", "12", "13", "14", "15", "16", "19", "22", "26", "28",
    "29", "30", "36", "40", "42", "43", "45", "46", "47", "50", "51", "52",
}

STUB_PREFIXES = (
    "Instructional content is defined",
    "Instructional content for this",
    "Any program",
)

def clean_code(val: str) -> str:
    """Strip Excel ="XX" quoting from CIP CSV values."""
    return val.strip().replace('="', "").replace('"', "")

def main():
    df = pd.read_csv(INPUT_FILE, dtype=str)

    # Normalize column values
    df["CIPCode"] = df["CIPCode"].apply(clean_code)
    df["CIPFamily"] = df["CIPFamily"].apply(clean_code)
    df["CIPTitle"] = df["CIPTitle"].fillna("").str.strip()
    df["CIPDefinition"] = df["CIPDefinition"].fillna("").str.strip()

    # Derive 2-digit area
    df["CIPArea"] = df["CIPCode"].str.split(".").str[0].str.zfill(2)

    # Filter 1: specific-level only (suffix does not end in 00, and has a decimal)
    has_decimal = df["CIPCode"].str.contains(r"\.", regex=True)
    not_stub_code = ~df["CIPCode"].str.endswith("00")
    df = df[has_decimal & not_stub_code].copy()

    # Filter 2: exclude residency/apprenticeship areas
    df = df[~df["CIPArea"].isin({"60", "61"})].copy()

    # Filter 3: exclude stub definitions
    is_stub = (
        df["CIPDefinition"].str.startswith(STUB_PREFIXES)
        | (df["CIPDefinition"].str.len() < 50)
    )
    df = df[~is_stub].copy()

    # Filter 4: keep selected CIP areas for analysis scope
    df = df[df["CIPArea"].isin(SELECTED_AREAS)].copy()

    # Select and order output columns
    out = df[["CIPCode", "CIPArea", "CIPTitle", "CIPDefinition"]].reset_index(drop=True)

    out.to_csv(OUTPUT_FILE, index=False)

    print(f"Wrote {len(out)} rows to {OUTPUT_FILE}")
    print(f"Areas ({out['CIPArea'].nunique()}): {sorted(out['CIPArea'].unique())}")

if __name__ == "__main__":
    main()

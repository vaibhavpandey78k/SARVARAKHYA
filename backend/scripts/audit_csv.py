"""Quick pre-ingestion audit required by the SARVARAKHYA backend brief."""
import sys
from pathlib import Path
import pandas as pd

REQUIRED = ["ID", "EventDate", "Employer", "Final Narrative"]

def main(path: str):
    p = Path(path)
    df = pd.read_csv(p, low_memory=False)
    print(f"rows={len(df):,}")
    print(f"columns={len(df.columns)}")
    print(f"duplicate_IDs={df['ID'].duplicated().sum():,}" if 'ID' in df else "duplicate_IDs=unavailable")
    missing = df.isna().sum().sort_values(ascending=False)
    print("top_missing_fields:")
    print(missing.head(10).to_string())
    if "EventDate" in df:
        dates = pd.to_datetime(df["EventDate"], errors="coerce")
        print(f"date_min={dates.min()}")
        print(f"date_max={dates.max()}")
        print(f"invalid_dates={dates.isna().sum():,}")
    if "Final Narrative" in df:
        lengths = df["Final Narrative"].fillna("").astype(str).str.len()
        print(f"narrative_min={lengths.min()}")
        print(f"narrative_median={lengths.median():.0f}")
        print(f"narrative_max={lengths.max()}")
        print(f"narrative_under_5={int((lengths < 5).sum()):,}")
    for col in ("Latitude", "Longitude"):
        if col in df:
            nums = pd.to_numeric(df[col], errors="coerce")
            bad = ((nums < (-90 if col == "Latitude" else -180)) | (nums > (90 if col == "Latitude" else 180))).sum()
            print(f"invalid_{col}={int(bad):,}")
    print("missing_required_columns=" + ",".join(c for c in REQUIRED if c not in df.columns) or "none")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/audit_csv.py path/to/data.csv")
    main(sys.argv[1])


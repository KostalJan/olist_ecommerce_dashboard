from pathlib import Path

# <project_root>/src/olist_dash/io/paths.py
# parents: [0]=io, [1]=olist_dash, [2]=src, [3]=<project_root>
ROOT = Path(__file__).resolve().parents[3]

DATA = ROOT / "data"
RAW = DATA / "raw"
INTERIM = DATA / "interim"
PROCESSED = DATA / "processed"
REPORTS = ROOT / "reports"

for p in [RAW, INTERIM, PROCESSED, REPORTS]:
    p.mkdir(parents=True, exist_ok=True)

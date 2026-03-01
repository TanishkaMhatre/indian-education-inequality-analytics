import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def read_csv_smart(path: Path) -> pd.DataFrame:
    """Read CSV with encoding fallback."""
    try:
        return pd.read_csv(path)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin1")

def clean_colname(c: str) -> str:
    """Normalize column names: remove weird chars, extra spaces."""
    c = c.replace("\u00a0", " ")
    c = re.sub(r"\s+", " ", c).strip()
    # fix common mojibake for apostrophe / special chars
    c = c.replace("Ã¢â‚¬â„¢", "'").replace("Ã¢â¬â", "").replace("Ã¢â", "")
    return c

def normalize_state(s: str) -> str:
    """Normalize state names across files."""
    if pd.isna(s):
        return s
    s = str(s).strip()

    replacements = {
        "Andaman & Nicobar Islands": "Andaman and Nicobar Islands",
        "Dadra & Nagar Haveli": "Dadra and Nagar Haveli",
        "Jammu & Kashmir": "Jammu and Kashmir",
        "NCT of Delhi": "Delhi",
        "Orissa": "Odisha",
        "Pondicherry": "Puducherry",
        "Uttaranchal": "Uttarakhand",
    }
    return replacements.get(s, s)

def pick(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    """Pick + rename columns if present."""
    cols = {}
    for old, new in mapping.items():
        if old in df.columns:
            cols[old] = new
    if not cols:
        return pd.DataFrame()
    return df[list(cols.keys())].rename(columns=cols)

def infra_percent(file_name: str, percent_col_contains: str, new_col: str) -> pd.DataFrame:
    """
    Load a state-level infra file and extract a % column using substring match (case-insensitive).
    """
    path = DATA / file_name
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    df = read_csv_smart(path)
    df.columns = [clean_colname(c) for c in df.columns]

    if "State" not in df.columns:
        raise ValueError(f"'State' column not found in {file_name}. Columns: {df.columns.tolist()}")

    df["State"] = df["State"].apply(normalize_state)

    # find matching percent column
    target = percent_col_contains.lower()
    percent_cols = [c for c in df.columns if target in c.lower()]

    if not percent_cols:
        # debug help: show columns if mismatch happens
        raise ValueError(
            f"Could not find a column containing:\n  '{percent_col_contains}'\n"
            f"in file {file_name}.\nAvailable columns:\n  {df.columns.tolist()}"
        )

    pcol = percent_cols[0]  # best match
    return df[["State", pcol]].rename(columns={pcol: new_col})

# ----------------------------
# 1) Core: Literacy + rural/urban enrolment (UDISE statewise secondary)
# ----------------------------
statewise_path = DATA / "2015_16_Statewise_Secondary.csv"
if not statewise_path.exists():
    raise FileNotFoundError(f"Missing: {statewise_path}")

statewise = read_csv_smart(statewise_path)
statewise.columns = [clean_colname(c) for c in statewise.columns]

core = pick(statewise, {
    "statname": "State",
    "literacy_rate": "Literacy_Total",
    "male_literacy_rate": "Literacy_Male",
    "female_literacy_rate": "Literacy_Female",
    "enr_r_all": "Enrol_Rural_All",
    "enr_u_all": "Enrol_Urban_All",
    "tot_population": "Total_Population",
    "urban_population": "Urban_Population",
    "sexratio": "Sex_Ratio",
    "sc_population": "SC_Population",
    "st_population": "ST_Population",
})

if core.empty:
    raise ValueError("Core dataset became empty. Check columns in 2015_16_Statewise_Secondary.csv")

core["State"] = core["State"].apply(normalize_state)

# ----------------------------
# 2) Add: Total enrolment split (small file)
# ----------------------------
enrol_path = DATA / "student-enrollment.csv"
if not enrol_path.exists():
    raise FileNotFoundError(f"Missing: {enrol_path}")

enrol = read_csv_smart(enrol_path)
enrol.columns = [clean_colname(c) for c in enrol.columns]
enrol["State"] = enrol["State"].apply(normalize_state)

enrol_small = pick(enrol, {
    "State": "State",
    "Enrolment - All Types of Management - Total (Pre-primary to 12)": "Enrol_Total_PrePri_12",
    "Enrolment - All Types of Management - Elementary (1-8)": "Enrol_Elementary_1_8",
    "Enrolment - All Types of Management - Secondary (9-10)": "Enrol_Secondary_9_10",
    "Enrolment - All Types of Management - Higher Secondary (11-12)": "Enrol_HS_11_12",
})

# ----------------------------
# 3) Add: Infrastructure % (internet, electricity, library, handwash)
# ----------------------------
internet = infra_percent(
    "internet-facility.csv",
    "% of Schools with Internet Facility available - All Management",
    "Pct_Internet_AllMgmt"
)

electricity = infra_percent(
    "electricity-availability.csv",
    "% of Schools with Electricity Connection - All Management",
    "Pct_Electricity_AllMgmt"
)

library = infra_percent(
    "library-facility.csv",
    "% of Schools with Library Facility - All Management",
    "Pct_Library_AllMgmt"
)

handwash = infra_percent(
    "handwash-availability.csv",
    "% of Schools with Hand Wash Facility - All Management",
    "Pct_Handwash_AllMgmt"
)

# ----------------------------
# 4) Add: Vocational (NSQF) adoption rate
# ----------------------------
voc_path = DATA / "vocational-courses-taken.csv"
if not voc_path.exists():
    raise FileNotFoundError(f"Missing: {voc_path}")

voc = read_csv_smart(voc_path)
voc.columns = [clean_colname(c) for c in voc.columns]
voc["State"] = voc["State"].apply(normalize_state)

voc_small = pick(voc, {
    "State": "State",
    "Number of Secondary and Higher Secondary Schools - All Management": "NSQF_SecHS_TotalSchools",
    "Number of Secondary and Higher Secondary Schools Having Vocational Courses under NSQF at Secondary/ Higher Secondary Level - All Management": "NSQF_SecHS_SchoolsWithVoc",
})

# ----------------------------
# 5) Merge everything (State key)
# ----------------------------
master = core.merge(enrol_small, on="State", how="left")
for part in [internet, electricity, library, handwash, voc_small]:
    master = master.merge(part, on="State", how="left")

# ----------------------------
# 6) Feature Engineering: Inequality metrics (Truth-style)
# ----------------------------
master["Gender_Gap_Literacy"] = master["Literacy_Male"] - master["Literacy_Female"]

# Avoid divide-by-zero
den = (master["Enrol_Urban_All"] + master["Enrol_Rural_All"]).replace(0, pd.NA)
master["Rural_Urban_Enrol_Divide"] = (master["Enrol_Urban_All"] - master["Enrol_Rural_All"]) / den

# Transition loss proxy (bigger = worse)
master["Transition_Loss_1_8_to_9_10"] = 1 - (master["Enrol_Secondary_9_10"] / master["Enrol_Elementary_1_8"]).replace([pd.NA, pd.NaT], pd.NA)

# NSQF adoption rate
master["Pct_SecHS_With_Voc"] = (master["NSQF_SecHS_SchoolsWithVoc"] / master["NSQF_SecHS_TotalSchools"]) * 100

# Infra index (avg)
master["Infra_Index"] = master[[
    "Pct_Internet_AllMgmt",
    "Pct_Electricity_AllMgmt",
    "Pct_Library_AllMgmt",
    "Pct_Handwash_AllMgmt"
]].mean(axis=1)

# Education Inequality Index (higher = worse)
master["Education_Inequality_Index"] = (
    0.35 * master["Transition_Loss_1_8_to_9_10"].clip(lower=0) * 100 +
    0.30 * master["Gender_Gap_Literacy"].clip(lower=0) +
    0.20 * (master["Rural_Urban_Enrol_Divide"].abs() * 100) +
    0.15 * (100 - master["Infra_Index"])
)

# ----------------------------
# 7) Save outputs
# ----------------------------
master = master.sort_values("Education_Inequality_Index", ascending=False)

out_csv = OUT / "master_state_education_inequality.csv"
master.to_csv(out_csv, index=False)

print("✅ Master dataset created:", out_csv)
print("\nTop 10 worst states by Education_Inequality_Index:")
print(
    master[[
        "State",
        "Education_Inequality_Index",
        "Gender_Gap_Literacy",
        "Transition_Loss_1_8_to_9_10",
        "Infra_Index"
    ]].head(10)
)
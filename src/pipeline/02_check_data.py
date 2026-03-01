import pandas as pd
import os

# Path to data folder
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data")

# List all CSV files
files = [f for f in os.listdir(DATA_PATH) if f.endswith(".csv")]

print("\n📂 CSV Files Found:")
for f in files:
    print(" -", f)

print("\n" + "="*70)

# Read and inspect each file
for file in files:
    print(f"\n🔎 Checking: {file}")
    print("-"*60)
    
    df = pd.read_csv(os.path.join(DATA_PATH, file), encoding="latin1")
    
    print("Shape:", df.shape)
    print("\nColumns:")
    print(list(df.columns))
    
    print("\nMissing Values:")
    print(df.isnull().sum().sort_values(ascending=False).head(10))
    
    print("\nFirst 3 Rows:")
    print(df.head(3))
    
    print("\n" + "="*70)
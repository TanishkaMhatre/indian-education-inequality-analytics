import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "outputs" / "master_state_education_inequality.csv"

df = pd.read_csv(MASTER)

print("\n===== TOP 5 HIGHEST INEQUALITY STATES =====")
print(df.sort_values("Education_Inequality_Index", ascending=False)
      [["State", "Education_Inequality_Index"]]
      .head(5))

print("\n===== TOP 5 LOWEST INEQUALITY STATES =====")
print(df.sort_values("Education_Inequality_Index", ascending=True)
      [["State", "Education_Inequality_Index"]]
      .head(5))

print("\n===== HIGHEST GENDER GAP STATES =====")
print(df.sort_values("Gender_Gap_Literacy", ascending=False)
      [["State", "Gender_Gap_Literacy"]]
      .head(5))

print("\n===== HIGHEST TRANSITION LOSS STATES =====")
print(df.sort_values("Transition_Loss_1_8_to_9_10", ascending=False)
      [["State", "Transition_Loss_1_8_to_9_10"]]
      .head(5))

print("\n===== LOWEST INFRASTRUCTURE STATES =====")
print(df.sort_values("Infra_Index", ascending=True)
      [["State", "Infra_Index"]]
      .head(5))

print("\n===== CORRELATION MATRIX =====")
print(df[[
    "Education_Inequality_Index",
    "Gender_Gap_Literacy",
    "Transition_Loss_1_8_to_9_10",
    "Infra_Index",
    "Rural_Urban_Enrol_Divide"
]].corr())
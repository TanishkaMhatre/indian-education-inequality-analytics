import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ---------- Setup ----------
ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "outputs" / "master_state_education_inequality.csv"
OUT = ROOT / "outputs" / "advanced_dashboards"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(MASTER)

# ---------- Theme ----------
sns.set_style("whitegrid")
plt.rcParams["figure.facecolor"] = "#f4f6f9"
plt.rcParams["axes.facecolor"] = "#f4f6f9"

PRIMARY = "#1f77b4"
SECONDARY = "#2ca02c"
ACCENT = "#ff7f0e"
DANGER = "#d62728"

# ---------- 1️⃣ Horizontal Bar (Better Ranking View) ----------
top10 = df.sort_values("Education_Inequality_Index", ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(
    data=top10,
    y="State",
    x="Education_Inequality_Index",
    palette="Blues_r"
)
plt.title("Top 10 States by Education Inequality Index", fontsize=14)
plt.tight_layout()
plt.savefig(OUT / "01_horizontal_ranking.png", dpi=200)
plt.close()

# ---------- 2️⃣ Heatmap (Correlation Analysis) ----------
plt.figure(figsize=(10,6))
corr = df[[
    "Education_Inequality_Index",
    "Gender_Gap_Literacy",
    "Transition_Loss_1_8_to_9_10",
    "Infra_Index",
    "Rural_Urban_Enrol_Divide"
]].corr()

sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Between Key Inequality Drivers")
plt.tight_layout()
plt.savefig(OUT / "02_correlation_heatmap.png", dpi=200)
plt.close()

# ---------- 3️⃣ Pie Chart (Infrastructure Composition Example) ----------
avg_infra = {
    "Internet": df["Pct_Internet_AllMgmt"].mean(),
    "Electricity": df["Pct_Electricity_AllMgmt"].mean(),
    "Library": df["Pct_Library_AllMgmt"].mean(),
    "Handwash": df["Pct_Handwash_AllMgmt"].mean()
}

plt.figure(figsize=(7,7))
plt.pie(
    avg_infra.values(),
    labels=avg_infra.keys(),
    autopct="%1.1f%%",
    colors=[PRIMARY, SECONDARY, ACCENT, DANGER]
)
plt.title("Average School Infrastructure Distribution (All States)")
plt.savefig(OUT / "03_infrastructure_pie.png", dpi=200)
plt.close()

# ---------- 4️⃣ Table Export (Professional Ranking Table) ----------
ranking_table = df[[
    "State",
    "Education_Inequality_Index",
    "Gender_Gap_Literacy",
    "Transition_Loss_1_8_to_9_10",
    "Infra_Index"
]].sort_values("Education_Inequality_Index", ascending=False)

ranking_table.to_csv(OUT / "state_ranking_table.csv", index=False)

print("✅ Advanced dashboards saved to:", OUT)
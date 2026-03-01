import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
master_path = ROOT / "outputs" / "master_state_education_inequality.csv"
FIG = ROOT / "outputs" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(master_path)

def bar_top10(col, title, filename, ascending=False):
    top = df.sort_values(col, ascending=ascending).head(10)
    plt.figure(figsize=(10, 5))
    plt.bar(top["State"], top[col])
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(FIG / filename, dpi=200)
    plt.close()

# 1) Worst inequality
bar_top10("Education_Inequality_Index",
          "Top 10 States with Highest Education Inequality Index (Higher = Worse)",
          "01_top10_inequality.png", ascending=False)

# 2) Gender gap
bar_top10("Gender_Gap_Literacy",
          "Top 10 States with Highest Literacy Gender Gap (Male - Female)",
          "02_top10_gender_gap.png", ascending=False)

# 3) Transition loss proxy
bar_top10("Transition_Loss_1_8_to_9_10",
          "Top 10 States with Highest Transition Loss (1-8 to 9-10) — Proxy Dropout",
          "03_top10_transition_loss.png", ascending=False)

# 4) Infrastructure poor
bar_top10("Infra_Index",
          "Bottom 10 States by School Infrastructure Index (Internet+Electricity+Library+Handwash)",
          "04_bottom10_infra.png", ascending=True)

print("✅ Charts saved in:", FIG)
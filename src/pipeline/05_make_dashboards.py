import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "outputs" / "master_state_education_inequality.csv"
OUTDIR = ROOT / "outputs" / "dashboards"
OUTDIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(MASTER)

def topn(col, n=10, ascending=False):
    return df.sort_values(col, ascending=ascending).head(n)[["State", col]]

def bottomn(col, n=10):
    return df.sort_values(col, ascending=True).head(n)[["State", col]]

def bar(ax, data, x, y, title):
    ax.bar(data[x], data[y])
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", alpha=0.3)

# -------------------------
# DASHBOARD PAGE 1: Ranking + Key Drivers
# -------------------------
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(2, 2)

ax1 = fig.add_subplot(gs[0, 0])
d1 = topn("Education_Inequality_Index", 10, ascending=False)
bar(ax1, d1, "State", "Education_Inequality_Index", "Top 10 States: Highest Education Inequality (Higher = Worse)")

ax2 = fig.add_subplot(gs[0, 1])
d2 = bottomn("Education_Inequality_Index", 10)
bar(ax2, d2, "State", "Education_Inequality_Index", "Bottom 10 States: Lowest Education Inequality (Better)")

ax3 = fig.add_subplot(gs[1, 0])
d3 = topn("Gender_Gap_Literacy", 10, ascending=False)
bar(ax3, d3, "State", "Gender_Gap_Literacy", "Top 10 States: Literacy Gender Gap (Male - Female)")

ax4 = fig.add_subplot(gs[1, 1])
d4 = topn("Transition_Loss_1_8_to_9_10", 10, ascending=False)
bar(ax4, d4, "State", "Transition_Loss_1_8_to_9_10", "Top 10 States: Transition Loss (1-8 → 9-10) Proxy Dropout")

fig.suptitle("Indian Education Inequality Dashboard — Page 1", fontsize=18)
fig.tight_layout(rect=[0, 0.02, 1, 0.95])
fig.savefig(OUTDIR / "dashboard_page_1.png", dpi=200)
plt.close(fig)

# -------------------------
# DASHBOARD PAGE 2: Infrastructure + Rural-Urban Divide
# -------------------------
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(2, 2)

ax1 = fig.add_subplot(gs[0, 0])
d1 = bottomn("Infra_Index", 10)
bar(ax1, d1, "State", "Infra_Index", "Bottom 10 States: Infrastructure Index (Internet+Electricity+Library+Handwash)")

ax2 = fig.add_subplot(gs[0, 1])
d2 = topn("Pct_Internet_AllMgmt", 10, ascending=False)
bar(ax2, d2, "State", "Pct_Internet_AllMgmt", "Top 10 States: % Schools with Internet (All Management)")

ax3 = fig.add_subplot(gs[1, 0])
d3 = bottomn("Pct_Electricity_AllMgmt", 10)
bar(ax3, d3, "State", "Pct_Electricity_AllMgmt", "Bottom 10 States: % Schools with Electricity (All Management)")

ax4 = fig.add_subplot(gs[1, 1])
d4 = topn("Rural_Urban_Enrol_Divide", 10, ascending=False)
bar(ax4, d4, "State", "Rural_Urban_Enrol_Divide", "Top 10: Rural–Urban Enrollment Divide (Share Difference)")

fig.suptitle("Indian Education Inequality Dashboard — Page 2", fontsize=18)
fig.tight_layout(rect=[0, 0.02, 1, 0.95])
fig.savefig(OUTDIR / "dashboard_page_2.png", dpi=200)
plt.close(fig)

print("✅ Dashboards saved to:", OUTDIR)
print("Files: dashboard_page_1.png, dashboard_page_2.png")
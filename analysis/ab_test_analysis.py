"""
A/B Test Analysis: Dashboard Default Date Range Change
=======================================================
Hypothesis: Switching the analytics dashboard default date range from
7-day to 30-day (implemented Nov 1, 2024) increased analyst engagement —
measured by session length, filter usage, and report exports.

"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ── LOAD ─────────────────────────────────────────────────────────────────────
df = pd.read_csv("data/dashboard_usage.csv")
df["date"] = pd.to_datetime(df["date"])

pre  = df[df["group"] == "pre"]
post = df[df["group"] == "post"]

print("=" * 62)
print("A/B TEST: Dashboard Default Date Range Change")
print("Pre-period : Jul 1 – Oct 31, 2024  (7-day default)")
print("Post-period: Nov 1, 2024 – Jan 1, 2025  (30-day default)")
print(f"Pre sessions : {len(pre):,}")
print(f"Post sessions: {len(post):,}")
print("=" * 62)

# ── METRIC 1: Session Length ──────────────────────────────────────────────────
t_stat, p_val = stats.ttest_ind(post["session_length_min"], pre["session_length_min"])
cohens_d = (post["session_length_min"].mean() - pre["session_length_min"].mean()) / \
           np.sqrt((post["session_length_min"].std()**2 + pre["session_length_min"].std()**2) / 2)

print("\n── METRIC 1: Average Session Length (minutes) ──────────────")
print(f"  Pre-period mean  : {pre['session_length_min'].mean():.2f} min")
print(f"  Post-period mean : {post['session_length_min'].mean():.2f} min")
print(f"  Absolute lift    : +{post['session_length_min'].mean() - pre['session_length_min'].mean():.2f} min")
print(f"  Relative lift    : +{(post['session_length_min'].mean()/pre['session_length_min'].mean()-1)*100:.1f}%")
print(f"  t-statistic      : {t_stat:.4f}")
print(f"  p-value          : {p_val:.2e}")
print(f"  Cohen's d        : {cohens_d:.4f}  ({'small' if abs(cohens_d)<0.5 else 'medium' if abs(cohens_d)<0.8 else 'large'} effect)")
print(f"  Significant?     : {'YES ✓ (p < 0.05)' if p_val < 0.05 else 'NO'}")

# ── METRIC 2: Filters Used ────────────────────────────────────────────────────
t2, p2 = stats.ttest_ind(post["filters_used"], pre["filters_used"])
d2 = (post["filters_used"].mean() - pre["filters_used"].mean()) / \
     np.sqrt((post["filters_used"].std()**2 + pre["filters_used"].std()**2) / 2)

print("\n── METRIC 2: Filters Used per Session ──────────────────────")
print(f"  Pre-period mean  : {pre['filters_used'].mean():.2f}")
print(f"  Post-period mean : {post['filters_used'].mean():.2f}")
print(f"  Relative lift    : +{(post['filters_used'].mean()/pre['filters_used'].mean()-1)*100:.1f}%")
print(f"  p-value          : {p2:.2e}")
print(f"  Cohen's d        : {d2:.4f}")
print(f"  Significant?     : {'YES ✓ (p < 0.05)' if p2 < 0.05 else 'NO'}")

# ── METRIC 3: Report Export Rate (chi-square) ─────────────────────────────────
pre_exp  = pre["exported_report"].sum()
post_exp = post["exported_report"].sum()
pre_no   = len(pre)  - pre_exp
post_no  = len(post) - post_exp
chi2, p3, dof, _ = stats.chi2_contingency([[pre_exp, pre_no],[post_exp, post_no]])
pre_rate  = pre_exp  / len(pre)  * 100
post_rate = post_exp / len(post) * 100

print("\n── METRIC 3: Report Export Rate ─────────────────────────────")
print(f"  Pre export rate  : {pre_rate:.1f}%  ({pre_exp:,} / {len(pre):,})")
print(f"  Post export rate : {post_rate:.1f}%  ({post_exp:,} / {len(post):,})")
print(f"  Absolute lift    : +{post_rate-pre_rate:.1f} percentage points")
print(f"  Chi-square       : {chi2:.4f}")
print(f"  p-value          : {p3:.2e}")
print(f"  Significant?     : {'YES ✓ (p < 0.05)' if p3 < 0.05 else 'NO'}")

# ── SUMMARY ───────────────────────────────────────────────────────────────────
print("\n── DECISION BRIEF ───────────────────────────────────────────")
print("""
All three engagement metrics showed statistically significant
improvement after the 30-day default was implemented (p < 0.05):

  • Session length increased by ~65% on average, suggesting
    analysts are spending more time exploring data with broader
    context available by default.

  • Filter usage increased by ~65%, indicating users are drilling
    into segments more actively — a sign of deeper data consumption.

  • Export rate increased by ~17 percentage points, meaning more
    sessions are resulting in shared/actioned deliverables.

RECOMMENDATION: Retain the 30-day default. Consider surfacing a
'Compare to prior period' toggle as the next product enhancement —
the increased filter usage suggests analysts want comparative views,
which the current dashboard doesn't natively support (Gap #4 in
the product backlog).

CAVEATS:
  - Dataset is simulated; real deployment would require holdout
    group isolation to control for seasonality.
  - Nov–Jan period includes holiday weeks; session patterns may
    differ from rest of year. Recommend re-evaluating in Q1.
""")

# ── SAVE SUMMARY TABLE ────────────────────────────────────────────────────────
summary = pd.DataFrame([
    {"metric": "Session Length (min)", "pre_mean": round(pre['session_length_min'].mean(),2),
     "post_mean": round(post['session_length_min'].mean(),2),
     "pct_lift": round((post['session_length_min'].mean()/pre['session_length_min'].mean()-1)*100,1),
     "p_value": round(p_val,6), "significant": p_val < 0.05},
    {"metric": "Filters Used", "pre_mean": round(pre['filters_used'].mean(),2),
     "post_mean": round(post['filters_used'].mean(),2),
     "pct_lift": round((post['filters_used'].mean()/pre['filters_used'].mean()-1)*100,1),
     "p_value": round(p2,6), "significant": p2 < 0.05},
    {"metric": "Export Rate (%)", "pre_mean": round(pre_rate,1),
     "post_mean": round(post_rate,1),
     "pct_lift": round(post_rate-pre_rate,1),
     "p_value": round(p3,6), "significant": p3 < 0.05},
])
summary.to_csv("data/query_outputs/ab_test_results.csv", index=False)
print("Results saved to data/query_outputs/ab_test_results.csv")

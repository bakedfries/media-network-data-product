# Media Network Data Product Health Tracker

**Context:** A media streaming/advertising network (retail media framework) with 5 internal analytics pods. I was brought in as a shared analytics resource to audit the existing data product ecosystem, identify gaps, fix measurement inconsistencies, and improve analyst self-service capability.  
**Tools:** Python · SQL (SQLite) · SciPy · Pandas · Markdown · Jira (simulated)

---

## What This Project Demonstrates

This is an end-to-end data product analyst portfolio project covering every core responsibility in a product analytics role:

| Competency | Artifact |
|-----------|---------|
| Gap identification & backlog management | [`docs/gap_audit_backlog.md`](docs/gap_audit_backlog.md) |
| Requirements documentation | [`docs/product_requirements_doc.md`](docs/product_requirements_doc.md) |
| SQL for data auditing and KPI reporting | [`sql/media_analytics_queries.sql`](sql/media_analytics_queries.sql) |
| A/B test / product experiment analysis | [`analysis/ab_test_analysis.py`](analysis/ab_test_analysis.py) |
| Governance & data dictionary | [`docs/data_dictionary.md`](docs/data_dictionary.md) |
| Agile delivery | [`docs/sprint_log.md`](docs/sprint_log.md) |

---

## The Business Problem

A gap audit of the media network analytics framework surfaced 8 data product issues causing real business impact:

- **CTR inconsistency** across 3 pods → advertiser billing disputes ($0 resolved after standardization)
- **Regional null exclusion** silently dropping ~12% of campaigns → $430K unreconciled in Finance
- **Completion rate discrepancy** between dashboard and SQL report → exec-level confusion in QBRs
- **No pacing alerts** → $82K in make-good credits in Q4 2024
- **No data dictionary** → new analysts spend 2–3 days reverse-engineering field definitions

All 8 gaps are logged in the [gap audit backlog](docs/gap_audit_backlog.md) with severity, business impact, owner, and resolution status.

---

## Dataset

Simulated retail media network data covering **Jul 1, 2024 – Jan 1, 2025** across 5 tables (14,926 total records):

| Table | Rows | Description |
|-------|------|-------------|
| `campaigns.csv` | 150 | Campaign metadata: advertiser, ad type, network, device, budget, dates |
| `daily_performance.csv` | 3,295 | Daily delivery: impressions, clicks, CTR, spend, completions, reach, frequency |
| `content.csv` | 80 | Content asset metadata: title, category, network, runtime |
| `content_daily.csv` | 5,692 | Daily content viewership: views, watch time, completion rate |
| `dashboard_usage.csv` | 5,709 | Analyst dashboard sessions: session length, filters used, exports |

Generate the dataset:
```bash
python data/generate.py
```

---

## SQL Query Library

12 validated queries covering core media analytics use cases:

| # | Query | Business Question |
|---|-------|------------------|
| Q01 | KPI Summary | Total spend, impressions, CTR, effective CPM |
| Q02 | By Advertiser | Which advertisers drive the most spend and engagement? |
| Q03 | WoW Trend | Is weekly impression delivery growing or declining? |
| Q04 | Category × Ad Type | Which content + format combos deliver the best CTR? |
| Q05 | Budget Pacing | Which campaigns are over/under-delivering? |
| Q06 | Device Breakdown | How does CTR and spend split across CTV, Mobile, Desktop, Tablet? |
| Q07 | Top Content | Which content assets drive the most viewership? |
| Q08 | Content Decay | How fast does viewership drop after publish? |
| Q09 | Regional | Which regions over/under-index on CTR vs. national average? |
| Q10 | Frequency Health | Which networks have audience burnout risk? |
| Q11 | CTR Anomalies | Which campaigns have tracking/tag fire issues? |
| Q12 | Monthly Rollup | One-row-per-month executive KPI summary |

Run all queries and save outputs:
```bash
python -c "
import sqlite3, pandas as pd
con = sqlite3.connect(':memory:')
for f,t in [('data/campaigns.csv','campaigns'),('data/daily_performance.csv','daily_performance'),
            ('data/content.csv','content'),('data/content_daily.csv','content_daily'),
            ('data/dashboard_usage.csv','dashboard_usage')]:
    pd.read_csv(f).to_sql(t, con, index=False)
# Then run individual queries from sql/media_analytics_queries.sql
"
```

---

## A/B Test: Dashboard Default Date Range Change

**Hypothesis:** Switching the analytics dashboard default date range from 7-day to 30-day (Nov 1, 2024) increases analyst engagement.

**Method:** Pre/post analysis across 3 engagement metrics (independent samples t-test for continuous metrics; chi-square for export rate).

**Results:**

| Metric | Pre (7-day default) | Post (30-day default) | Lift | p-value |
|--------|--------------------|-----------------------|------|---------|
| Session length | 5.11 min | 8.37 min | +63.9% | <0.001 |
| Filters used | 2.27 | 3.78 | +66.3% | <0.001 |
| Export rate | 21.6% | 38.0% | +16.4 pp | <0.001 |

All three metrics significant at p < 0.001. **Recommendation: retain 30-day default.**

Run the analysis:
```bash
python analysis/ab_test_analysis.py
```

---

## Sprint Summary

Managed delivery across 2 Agile sprints (4 weeks). 18 tickets closed, 4 of 8 gaps resolved.

| Sprint | Goal | Velocity |
|--------|------|----------|
| Sprint 1 | Audit, gap identification, SQL library, A/B test | 22/22 pts |
| Sprint 2 | Fix P0/P1 gaps, data dictionary, PRD for G-04 | 19/19 pts |

See full [sprint log](docs/sprint_log.md).

---

## Key Findings

1. **$430K in campaign spend was missing from all regional reports** due to a COALESCE bug — fixed in Sprint 2
2. **CTR variance of up to 40%** across pods from formula inconsistency — resolved by standardizing to IAB definition
3. **~11 analyst hours/week** being spent on manual Excel WoW comparisons — documented as G-04, scoped for Sprint 3
4. **30-day dashboard default** increased report exports by 16 percentage points — statistically significant, retained

---

## File Structure

```
media_network_project/
├── data/
│   ├── generate.py              # Dataset generation script
│   ├── campaigns.csv
│   ├── daily_performance.csv
│   ├── content.csv
│   ├── content_daily.csv
│   ├── dashboard_usage.csv
│   └── query_outputs/           # CSV outputs from all 12 SQL queries + A/B test
├── sql/
│   └── media_analytics_queries.sql   # 12 validated queries
├── analysis/
│   └── ab_test_analysis.py      # A/B test with t-test and chi-square
└── docs/
    ├── gap_audit_backlog.md     # 8 gaps logged with severity and resolution
    ├── product_requirements_doc.md  # PRD for Sprint 2 fixes
    ├── data_dictionary.md       # All 5 tables, all fields, KPI glossary
    └── sprint_log.md            # Sprint 1 + 2 tickets, velocity, retros
```

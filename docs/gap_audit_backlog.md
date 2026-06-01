# Media Network Analytics — Data Product Gap Audit
**Analyst:** Aakriti Dahal  
**Sprint:** Sprint 1 (Audit & Discovery)  
**Last Updated:** 2025-01-15  
**Status:** In Review

---

## How to Use This Document
Each gap was identified through stakeholder interviews, dashboard usage analysis, and direct data audits across the Media Network analytics framework. Gaps are logged with severity, estimated business impact, owner pod, and resolution status. This backlog feeds directly into the Sprint 2 build queue.

**Severity levels:**  
🔴 P0 — Blocking reporting or billing  
🟠 P1 — Causing measurement inconsistency across teams  
🟡 P2 — Reducing analyst efficiency or self-service capability  
🟢 P3 — Documentation / polish gaps

---

## Gap Registry

| # | Gap | Severity | Business Impact | Affected Teams | Status |
|---|-----|----------|-----------------|----------------|--------|
| G-01 | CTR definition inconsistent across pods | 🔴 P0 | Advertisers receive conflicting CTR figures depending on which team pulls the report | Ad Sales, Campaign Ops, Analytics | Open |
| G-02 | No pacing alert for under-delivery campaigns | 🟠 P1 | Under-delivering campaigns identified too late to recover, causing make-good spend | Campaign Ops, Finance | Open |
| G-03 | Content completion rate calculated differently in Tableau vs. downstream SQL | 🟠 P1 | Executives see different completion rates in dashboard vs. weekly email report | Content, Analytics | Open |
| G-04 | Dashboard lacks period-over-period comparison view | 🟡 P2 | Analysts manually export data to Excel to do WoW/MoM comparisons — avg 45 min overhead per report | Analytics, Ad Sales | Open |
| G-05 | `frequency` field undocumented — no agreed definition of unique user window | 🟡 P2 | Frequency capping decisions are based on inconsistently defined field; risk of audience overexposure | Audience, Campaign Ops | Open |
| G-06 | No data dictionary for the `campaigns` table | 🟡 P2 | New team members spend 2–3 days reverse-engineering field definitions on onboarding | All pods | Open |
| G-07 | Regional roll-up logic excludes campaigns without a `region` value | 🟠 P1 | ~12% of campaigns silently dropped from regional reports — national totals don't reconcile | Analytics, Finance | Open |
| G-08 | Dashboard usage not tracked — no visibility into adoption or active users | 🟡 P2 | Product team cannot measure whether dashboard changes improve engagement or identify power users | Analytics, Product | Resolved (Sprint 1) |

---

## Detailed Gap Write-Ups

### G-01 — CTR Definition Inconsistency 🔴 P0

**Observed:** Three different CTR calculations exist across pods:
- Ad Sales pod: `clicks / impressions`
- Campaign Ops: `clicks / served_impressions` (excludes viewable-only)
- Analytics dashboard: `total_interactions / reach`

**Impact:** Advertiser-facing reports show CTR variance of up to 40% for the same campaign depending on source. Has caused billing disputes on 2 campaigns in Q3 2024.

**Root cause:** No agreed KPI definition document at time of dashboard build. Each pod inherited a different legacy calculation.

**Proposed resolution:** Align on a single definition (`clicks / impressions`, consistent with IAB standard). Update all three surfaces. Add a KPI glossary page to the dashboard.

**Owner:** Analytics Lead + Campaign Ops  
**Estimated effort:** 3 days (SQL updates + dashboard change + stakeholder sign-off)

---

### G-02 — No Pacing Alerts for Under-Delivery 🟠 P1

**Observed:** Campaign pacing is only reviewed manually during weekly ops calls. No automated signal exists when a campaign falls below 85% of target delivery with more than 5 days remaining.

**Impact:** In Q4 2024, 14 campaigns ended under-delivered, requiring $82K in make-good credits. Early detection could have enabled pacing adjustments in time.

**Proposed resolution:** Build a daily pacing query (see Q05 in SQL library) and route campaigns flagged `UNDER` with >5 days remaining to a Slack alert or email digest. Establish 85% / 110% as the standard floor/ceiling thresholds.

**Owner:** Campaign Ops  
**Estimated effort:** 2 days (query + alert pipeline)

---

### G-03 — Completion Rate Discrepancy (Dashboard vs. SQL) 🟠 P1

**Observed:** The Tableau dashboard calculates completion rate as `completions / impressions`. The weekly SQL report uses `completions / views`. For content with high impression-but-low-view campaigns, this creates a 15–25% variance.

**Impact:** Content team uses the dashboard; the exec summary uses the SQL report. Leadership has flagged the discrepancy twice in QBRs.

**Proposed resolution:** Standardize on `completions / impressions` (aligns with ad server output). Update the SQL report. Document the change in the data dictionary with the rationale and effective date.

**Owner:** Analytics + Content Pod  
**Estimated effort:** 1 day

---

### G-04 — No Period-over-Period Comparison View 🟡 P2

**Observed:** Dashboard usage analysis (see A/B test) showed that post the 30-day default change, filter usage increased 66% — analysts are clearly trying to build comparisons manually. No native WoW or MoM toggle exists.

**Impact:** Estimated 45 minutes of manual Excel work per analyst per weekly report cycle. Across ~15 regular users, that's ~11 hours/week of avoidable overhead.

**Proposed resolution:** Add a "Compare to prior period" date-range selector to the dashboard header. Applies to all KPI tiles and trend charts.

**Owner:** Analytics + BI Engineering  
**Estimated effort:** 5 days (dashboard update + QA)

---

### G-05 — `frequency` Field Undocumented 🟡 P2

**Observed:** The `frequency` column in `daily_performance` has no definition in any documentation. Stakeholder interviews revealed three different mental models: daily unique user window, campaign-lifetime window, and 7-day rolling window.

**Impact:** Frequency capping decisions vary by pod. Risk of audience overexposure and advertiser complaints.

**Proposed resolution:** Define `frequency` as a 7-day rolling unique user window (aligns with industry standard). Document in data dictionary. Add a tooltip to the dashboard.

**Owner:** Data Engineering + Analytics  
**Estimated effort:** 1 day (documentation) + possible back-fill depending on source definition

---

### G-06 — No Data Dictionary for `campaigns` Table 🟡 P2

**Observed:** None of the 11 fields in the `campaigns` table have a documented definition, accepted values list, or owner. New analysts report spending 2–3 days reverse-engineering field meaning on onboarding.

**Proposed resolution:** Create a data dictionary (see `docs/data_dictionary.md`) covering all 5 tables: field name, data type, definition, example values, owner, and last validated date.

**Owner:** Analytics (this project)  
**Estimated effort:** 1 day

---

### G-07 — Regional Roll-Up Silently Drops ~12% of Campaigns 🟠 P1

**Observed:** SQL audit found that campaigns with `NULL` or `''` in the `region` field are excluded from GROUP BY aggregations in the regional report. These 18 campaigns represent approximately $430K in spend that does not appear in any regional breakdown.

**Impact:** National spend totals do not reconcile with sum of regional spend. Finance has been manually patching this gap.

**Proposed resolution:** Add `COALESCE(region, 'Unassigned')` to all regional queries. Add a data validation check to flag new campaigns with missing region at ingestion. Document the fix.

**Owner:** Analytics + Data Engineering  
**Estimated effort:** Half day

---

### G-08 — Dashboard Usage Not Tracked --> Resolved

**Resolution:** Dashboard usage logging was implemented as part of this project (see `data/dashboard_usage.csv` and A/B test analysis). Sessions, filter usage, and export events are now tracked per user per day. Adoption baseline established for ongoing monitoring.

---

## Backlog Priority Queue (Sprint 2)

| Priority | Gap | Effort | Owner |
|----------|-----|--------|-------|
| 1 | G-01 CTR definition | 3 days | Analytics Lead |
| 2 | G-07 Regional null exclusion | 0.5 days | Analytics |
| 3 | G-03 Completion rate discrepancy | 1 day | Analytics |
| 4 | G-02 Pacing alerts | 2 days | Campaign Ops |
| 5 | G-06 Data dictionary | 1 day | Analytics |
| 6 | G-05 Frequency definition | 1 day | Data Engineering |
| 7 | G-04 Period comparison view | 5 days | BI Engineering |

# Agile Sprint Log — Media Network Data Product Health Tracker
**Analyst:** Aakriti Dahal  
**Tool:** Jira (simulated)  
**Methodology:** Scrum, 2-week sprints  
**Project Duration:** Sprint 1 (Jan 1–14) + Sprint 2 (Jan 15–28)

---

## Sprint 1 — Audit & Discovery
**Goal:** Understand the current state of the media network analytics data products, identify gaps, and establish baselines.

### Sprint 1 Backlog

| Ticket | Task | Points | Status |
|--------|------|--------|--------|
| MN-01 | Audit all 5 data tables for schema issues, nulls, and undocumented fields | 3 | Done |
| MN-02 | Interview stakeholders from Analytics, Campaign Ops, Content, and Finance pods | 3 |  Done |
| MN-03 | Run gap audit; log findings in gap_audit_backlog.md | 2 |  Done |
| MN-04 | Write 12 SQL queries covering core media analytics KPIs | 5 |  Done |
| MN-05 | Implement dashboard usage tracking (G-08) | 3 |  Done |
| MN-06 | Run A/B test analysis on default date range change | 3 |  Done |
| MN-07 | Generate simulated dataset for project environment | 2 |  Done |
| MN-08 | Prioritize Sprint 2 backlog with stakeholders | 1 |  Done |

**Sprint 1 Velocity:** 22 points completed / 22 planned  
**Retrospective notes:**  
- G-07 (regional null drop) was a surprise find during SQL audit — flagged mid-sprint and added to backlog without disrupting sprint goal  
- Stakeholder interview with Finance uncovered the $430K unreconciled spend figure — raised severity of G-07 from P2 to P1  
- A/B test results were stronger than expected; recommend sharing with BI Engineering as input for the G-04 comparison view build

---

## Sprint 2 — Fix & Document
**Goal:** Resolve the top 3 P0/P1 data product gaps, publish the data dictionary, and deliver a clean handoff to BI Engineering for the G-04 dashboard enhancement.

### Sprint 2 Backlog

| Ticket | Task | Points | Status |
|--------|------|--------|--------|
| MN-09 | Standardize CTR formula across all SQL report templates (G-01) | 3 |  Done |
| MN-10 | Add KPI Glossary page to dashboard (G-01) | 2 |  Done |
| MN-11 | Fix regional COALESCE logic in all regional queries (G-07) | 1 |  Done |
| MN-12 | Add data validation check for NULL region at ingestion (G-07) | 2 |  Done |
| MN-13 | Get Finance sign-off on regional reconciliation (G-07) | 1 |  Done |
| MN-14 | Standardize completion rate to `completions/impressions` (G-03) | 1 |  Done |
| MN-15 | Publish full data dictionary covering all 5 tables (G-06) | 3 |  Done |
| MN-16 | QA all 3 fixes against 10 representative campaigns | 2 |  Done |
| MN-17 | Write G-04 requirements in PRD for BI Engineering handoff | 3 |  Done |
| MN-18 | Sprint 2 stakeholder demo + retrospective | 1 |  Done |

**Sprint 2 Velocity:** 19 points completed / 19 planned  
**Retrospective notes:**  
- MN-12 (ingestion validation) took longer than estimated due to upstream pipeline dependency; resolved with a post-load reconciliation check as interim solution  
- Finance sign-off on MN-13 required two rounds of review; build in stakeholder review buffer in future sprints  
- G-04 PRD handed off to BI Engineering with A/B test data as supporting evidence — prioritized for Sprint 3

---

## Sprint 3 — Planned (not yet started)

| Ticket | Task | Notes |
|--------|------|-------|
| MN-19 | G-04: Period-over-period comparison view | BI Engineering lead |
| MN-20 | G-05: Define and document `frequency` field (7-day window) | Data Engineering input needed |
| MN-21 | G-02: Pacing alert pipeline | Campaign Ops to own; analyst supports query |
| MN-22 | Dashboard adoption report: monthly active users, top features | Use dashboard_usage table |

---

## Project Summary

| Metric | Value |
|--------|-------|
| Total sprints completed | 2 |
| Total tickets closed | 18 |
| Data product gaps resolved | 4 of 8 (G-01, G-03, G-07, G-08) |
| SQL queries written & validated | 12 |
| Tables documented | 5 |
| A/B tests conducted | 1 |
| Analyst hours saved/week (est.) | ~9 hours (G-04 partially; G-01, G-03, G-07 resolved) |
| Sprint velocity | 22 / 19 (sprints 1–2) |

# Product Requirements Document
## Media Network Analytics Dashboard — Sprint 2 Enhancements

**Author:** Aakriti Dahal, Data Product Analyst  
**Version:** 1.0  
**Status:** Draft — Pending Stakeholder Sign-off  
**Stakeholders:** Analytics Lead, Campaign Ops Manager, BI Engineering, Content Pod Lead  
**Target Release:** Sprint 2 (2-week cycle)

---

## 1. Background & Problem Statement

The Media Network analytics dashboard currently serves ~60 internal analysts across 5 pods. A gap audit (Jan 2025) identified 7 data product gaps causing measurement inconsistency, reporting overhead, and billing disputes. This PRD covers the top 3 gaps selected for Sprint 2 based on business impact, effort, and dependency order.

**Gaps addressed in this PRD:**
- G-01: CTR definition inconsistency (P0)
- G-07: Regional roll-up silently drops ~12% of campaigns (P1)
- G-03: Completion rate discrepancy between dashboard and SQL report (P1)

---

## 2. Goals & Success Metrics

| Goal | Metric | Baseline | Target | Measurement Method |
|------|--------|----------|--------|--------------------|
| Single CTR definition across all pods | % of reports using standardized CTR formula | ~33% (1 of 3 pods) | 100% | Audit of SQL report templates post-sprint |
| Eliminate billing disputes from CTR variance | # of advertiser CTR escalations per quarter | 2 in Q3 2024 | 0 | Campaign Ops escalation log |
| Regional spend reconciles with national total | $ variance between national and sum-of-regional | ~$430K | <$1K | Monthly Finance reconciliation check |
| Completion rate consistent across surfaces | % difference between dashboard and SQL report | 15–25% | <1% | Spot-check on 10 campaigns post-fix |
| Analyst time saved on manual reconciliation | Hours/week spent on manual Excel patching | ~11 hrs/week | <2 hrs/week | Self-reported in analyst survey (n=15) |

---

## 3. User Stories

**G-01 — CTR Standardization**  
*As a Campaign Ops manager, I want all CTR figures to use the same formula across every report surface so that I can present consistent numbers to advertisers without cross-checking three sources.*

*As an Ad Sales analyst, I want to know which CTR definition is used on each report so that I can confidently answer advertiser questions without escalating to engineering.*

**G-07 — Regional Null Fix**  
*As a Finance analyst, I want national spend totals to equal the sum of all regional spend so that I can close the books without manual patching each month.*

*As a Campaign Ops analyst, I want campaigns without a region assigned to appear as "Unassigned" in regional reports rather than being silently dropped so that I have full visibility into delivery.*

**G-03 — Completion Rate Fix**  
*As a Content pod lead, I want the completion rate on the dashboard to match the number in the weekly exec email so that leadership and my team are working from the same figure.*

---

## 4. Functional Requirements

### 4.1 CTR Standardization (G-01)

| ID | Requirement | Priority |
|----|-------------|----------|
| F-01 | All CTR calculations across Campaign Ops SQL report, Ad Sales Tableau view, and Analytics dashboard must use: `clicks / impressions` | Must Have |
| F-02 | A KPI Glossary page must be added to the dashboard defining CTR, completion rate, frequency, reach, CPM, and ROAS with formula, data source, and effective date | Must Have |
| F-03 | Historical CTR values in the dashboard must be recalculated using the new formula back to Jul 1, 2024 | Must Have |
| F-04 | A changelog entry must be added to the dashboard footer noting the formula change date | Should Have |

### 4.2 Regional Null Fix (G-07)

| ID | Requirement | Priority |
|----|-------------|----------|
| F-05 | All GROUP BY queries on `region` must use `COALESCE(region, 'Unassigned')` | Must Have |
| F-06 | An "Unassigned" region row must appear in the regional breakdown table in the dashboard | Must Have |
| F-07 | A data validation check must be added to the campaign ingestion pipeline to flag new records with NULL region within 24 hours of load | Should Have |
| F-08 | Finance reconciliation report must be re-run using the corrected logic and signed off before release | Must Have |

### 4.3 Completion Rate Standardization (G-03)

| ID | Requirement | Priority |
|----|-------------|----------|
| F-09 | Completion rate must be defined as `completions / impressions` across dashboard and SQL report | Must Have |
| F-10 | The weekly SQL report template must be updated to match | Must Have |
| F-11 | The data dictionary must document the old vs. new formula, rationale, and effective date | Must Have |

---

## 5. Non-Functional Requirements

- All SQL changes must be peer-reviewed by one other analyst before merging
- Dashboard changes must be QA'd against 10 representative campaigns before release
- No breaking changes to existing report column names (downstream consumers exist)
- All changes must be documented in the data dictionary before the sprint closes

---

## 6. Out of Scope (Sprint 2)

- G-04 Period-over-period comparison view (BI Engineering dependency; Sprint 3)
- G-05 Frequency field redefinition (requires Data Engineering input; Sprint 3)
- G-02 Pacing alerts (Campaign Ops to own; parallel track)

---

## 7. Dependencies & Risks

| Dependency | Owner | Risk if Delayed |
|------------|-------|-----------------|
| BI Engineering availability for dashboard CTR update | BI Eng Lead | CTR fix delayed; can partially ship SQL-only fix |
| Finance sign-off on regional reconciliation | Finance Manager | G-07 fix ships but not formally closed |
| Stakeholder alignment on CTR formula (IAB standard) | Analytics Lead | Blocks F-01; must resolve in Sprint 2 kickoff |

---

## 8. Sprint Plan

**Sprint 2 — 2 weeks**

| Day | Task | Owner |
|-----|------|-------|
| 1 | Stakeholder kickoff: align on CTR formula | Analytics Lead |
| 1–2 | Update regional COALESCE fix across all queries | Aakriti |
| 2 | Run Finance reconciliation check; get sign-off | Aakriti + Finance |
| 3 | Update completion rate in SQL report + data dictionary | Aakriti |
| 3–5 | Dashboard CTR recalculation + KPI Glossary page | BI Engineering |
| 6–8 | QA: spot-check 10 campaigns across all 3 fixes | Aakriti |
| 9 | Stakeholder UAT | All pods |
| 10 | Release + changelog entry + retrospective | All |

---

## 9. Definition of Done

- [ ] All three gaps resolved and QA'd against defined success metrics
- [ ] Data dictionary updated with new formulas and effective dates
- [ ] Finance reconciliation sign-off documented
- [ ] KPI Glossary page live on dashboard
- [ ] Retrospective notes captured and filed
- [ ] Sprint 3 backlog pre-populated with G-04, G-05, G-02

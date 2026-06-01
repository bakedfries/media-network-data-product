# Data Dictionary — Media Network Analytics
**Owner:** Aakriti Dahal
**Last Validated:** 2025-01-15  
**Tables covered:** `campaigns`, `daily_performance`, `content`, `content_daily`, `dashboard_usage`

---

## Table: `campaigns`
*One row per campaign. Master reference for all campaign metadata.*

| Field | Type | Definition | Example | Accepted Values | Notes |
|-------|------|------------|---------|-----------------|-------|
| campaign_id | STRING | Unique campaign identifier | CMP0042 | CMP + 4-digit number | Primary key |
| advertiser | STRING | Advertiser brand name | AutoBrand_A | See advertiser lookup table | |
| ad_type | STRING | Format of the ad unit | Pre-roll | Pre-roll, Mid-roll, Display, Sponsored_Content | |
| network | STRING | Media network carrying the campaign | StreamMax | StreamMax, VisionPlus, PrimeView, NexGen, ArcLight | |
| content_category | STRING | Content genre the campaign runs against | Sports | Sports, News, Entertainment, Drama, Reality, Documentary | |
| region | STRING | Geographic target region | Midwest | Northeast, Southeast, Midwest, West, Southwest, **Unassigned** | NULLs treated as Unassigned per G-07 fix |
| device | STRING | Target device type | CTV | CTV, Mobile, Desktop, Tablet | |
| budget | FLOAT | Total campaign budget in USD | 125000.00 | >0 | |
| start_date | DATE | Campaign start date | 2024-08-15 | YYYY-MM-DD | |
| end_date | DATE | Campaign end date | 2024-09-12 | YYYY-MM-DD | Must be >= start_date |
| target_impressions | INTEGER | Contracted impression delivery goal | 4500000 | >0 | Derived from budget / target CPM at booking |

---

## Table: `daily_performance`
*One row per campaign per active day. Core fact table for all delivery reporting.*

| Field | Type | Definition | Example | Formula / Source | Notes |
|-------|------|------------|---------|-----------------|-------|
| campaign_id | STRING | FK to campaigns | CMP0042 | | |
| date | DATE | Reporting date | 2024-09-01 | | |
| impressions | INTEGER | Total ad impressions served | 48200 | Ad server count | |
| clicks | INTEGER | Total clicks on the ad unit | 144 | Ad server count | |
| **ctr** | FLOAT | Click-through rate | 0.0299 | `clicks / impressions` ⚠️ Standardized Nov 2024 | **Formula updated from legacy `interactions/reach` — see changelog** |
| spend | FLOAT | Total spend in USD for the day | 823.40 | `impressions / 1000 * cpm` | |
| cpm | FLOAT | Cost per thousand impressions | 17.08 | Contracted or dynamic rate | |
| completions | INTEGER | Ad views completed to 100% | 39200 | Ad server count | |
| **completion_rate** | FLOAT | % of impressions completed | 0.8133 | `completions / impressions` ⚠️ Standardized Nov 2024 | **Formula updated from legacy `completions/views` — see changelog** |
| reach | INTEGER | Unique users who saw the ad | 31500 | 7-day rolling unique user window | See G-05 for definition history |
| frequency | FLOAT | Average times a unique user saw the ad | 1.53 | `impressions / reach` | Calculated field; 7-day window |

---

## Table: `content`
*One row per content asset. Reference table for content performance analysis.*

| Field | Type | Definition | Example | Notes |
|-------|------|------------|---------|-------|
| content_id | STRING | Unique content asset identifier | CNT0017 | Primary key |
| title | STRING | Content title | Drama_Show_017 | |
| category | STRING | Content genre | Drama | Sports, News, Entertainment, Drama, Reality, Documentary |
| network | STRING | Network airing the content | VisionPlus | |
| publish_date | DATE | Date content first became available | 2024-08-22 | |
| episode_length_min | INTEGER | Runtime in minutes | 44 | 22, 44, 60, 90 |

---

## Table: `content_daily`
*One row per content asset per day. Tracks viewership and engagement over time.*

| Field | Type | Definition | Example | Notes |
|-------|------|------------|---------|-------|
| content_id | STRING | FK to content | CNT0017 | |
| date | DATE | Reporting date | 2024-09-01 | |
| views | INTEGER | Total views of the content asset | 182400 | Counts any view start, regardless of length |
| avg_watch_time_min | FLOAT | Average minutes watched per view | 31.4 | |
| completion_rate | FLOAT | Avg % of episode watched | 0.714 | `avg_watch_time_min / episode_length_min` |
| unique_viewers | INTEGER | Distinct users who started the content | 148900 | 7-day unique window |
| device | STRING | Device type for this row | CTV | CTV, Mobile, Desktop, Tablet |
| region | STRING | Region for this row | West | Northeast, Southeast, Midwest, West, Southwest |

---

## Table: `dashboard_usage`
*One row per user per day the dashboard was accessed. Used for product adoption tracking.*

| Field | Type | Definition | Example | Notes |
|-------|------|------------|---------|-------|
| user_id | STRING | Anonymized analyst identifier | USER042 | |
| date | DATE | Session date | 2024-11-14 | |
| group | STRING | Pre/post A/B test group | post | pre = 7-day default; post = 30-day default |
| session_length_min | FLOAT | Duration of dashboard session in minutes | 9.2 | |
| filters_used | INTEGER | Number of filter interactions in session | 4 | |
| exported_report | INTEGER | Whether a report was exported in session | 1 | 0 = no, 1 = yes |

---

## KPI Glossary

| KPI | Formula | Definition | Standard |
|-----|---------|------------|----------|
| CTR | `clicks / impressions` | Click-through rate | IAB standard |
| CPM | `spend / impressions * 1000` | Cost per thousand impressions | IAB standard |
| Completion Rate (ads) | `completions / impressions` | % of ad impressions played to 100% | IAB standard |
| Completion Rate (content) | `avg_watch_time / episode_length` | % of episode watched on average | Internal |
| Reach | Unique users, 7-day rolling window | Distinct users exposed to an ad or content asset | Internal |
| Frequency | `impressions / reach` | Average exposures per unique user | Internal |
| Pacing | `actual_impressions / target_impressions` | Delivery progress against contracted goal | Internal |
| ROAS | `revenue / spend` | Return on ad spend | Advertiser-provided revenue required |

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2025-01-15 | Initial data dictionary created | Aakriti Dahal |
| 2025-01-15 | CTR formula standardized to `clicks/impressions` across all surfaces (was `interactions/reach` in Ad Sales pod) | Aakriti Dahal |
| 2025-01-15 | Ad completion rate standardized to `completions/impressions` (was `completions/views` in SQL report) | Aakriti Dahal |
| 2025-01-15 | Region NULLs now treated as 'Unassigned' in all regional aggregations | Aakriti Dahal |

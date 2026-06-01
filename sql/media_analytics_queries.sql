-- ============================================================
-- Media Network Analytics — SQL Query Library
-- Analyst: Aakriti Dahal  |  Project: Data Product Health Tracker
-- Dataset: Simulated retail media network (Jul 2024 – Jan 2025)
-- Tables: campaigns, daily_performance, content, content_daily,
--         dashboard_usage
-- ============================================================


-- ── QUERY 1: Overall campaign KPI summary ───────────────────────────────────
-- Business question: What is total spend, impressions, clicks, and average
-- CTR across all campaigns in the dataset period?

SELECT
    COUNT(DISTINCT p.campaign_id)          AS total_campaigns,
    SUM(p.impressions)                     AS total_impressions,
    SUM(p.clicks)                          AS total_clicks,
    ROUND(SUM(p.spend), 2)                 AS total_spend,
    ROUND(AVG(p.ctr) * 100, 3)            AS avg_ctr_pct,
    ROUND(SUM(p.spend) /
          NULLIF(SUM(p.impressions),0)
          * 1000, 2)                       AS effective_cpm
FROM daily_performance p;


-- ── QUERY 2: Campaign performance by advertiser ──────────────────────────────
-- Business question: Which advertisers are driving the most spend and
-- impressions? Used to prioritize account reviews.

SELECT
    c.advertiser,
    COUNT(DISTINCT c.campaign_id)          AS campaigns,
    SUM(p.impressions)                     AS total_impressions,
    ROUND(SUM(p.spend), 2)                 AS total_spend,
    ROUND(AVG(p.ctr) * 100, 3)            AS avg_ctr_pct,
    ROUND(AVG(p.completion_rate) * 100, 2) AS avg_completion_rate_pct
FROM campaigns c
JOIN daily_performance p ON c.campaign_id = p.campaign_id
GROUP BY c.advertiser
ORDER BY total_spend DESC;


-- ── QUERY 3: Week-over-week impressions trend ────────────────────────────────
-- Business question: Is total inventory delivery growing or declining
-- week over week? Key leading indicator for revenue health.

SELECT
    strftime('%Y-W%W', date)               AS week,
    SUM(impressions)                       AS weekly_impressions,
    ROUND(SUM(spend), 2)                   AS weekly_spend,
    SUM(impressions) - LAG(SUM(impressions))
        OVER (ORDER BY strftime('%Y-W%W', date)) AS impressions_wow_delta,
    ROUND(
        (SUM(impressions) - LAG(SUM(impressions))
            OVER (ORDER BY strftime('%Y-W%W', date))) * 100.0
        / NULLIF(LAG(SUM(impressions))
            OVER (ORDER BY strftime('%Y-W%W', date)), 0)
    , 2)                                   AS impressions_wow_pct_change
FROM daily_performance
GROUP BY week
ORDER BY week;


-- ── QUERY 4: Performance by content category and ad type ────────────────────
-- Business question: Which content category + ad type combinations
-- deliver the highest CTR and completion rates? Informs inventory packaging.

SELECT
    c.content_category,
    c.ad_type,
    COUNT(DISTINCT c.campaign_id)          AS campaigns,
    SUM(p.impressions)                     AS impressions,
    ROUND(AVG(p.ctr) * 100, 3)            AS avg_ctr_pct,
    ROUND(AVG(p.completion_rate) * 100, 2) AS avg_completion_rate_pct,
    ROUND(AVG(p.cpm), 2)                  AS avg_cpm
FROM campaigns c
JOIN daily_performance p ON c.campaign_id = p.campaign_id
GROUP BY c.content_category, c.ad_type
ORDER BY avg_ctr_pct DESC;


-- ── QUERY 5: Budget pacing — over/under-delivery flag ───────────────────────
-- Business question: Which campaigns are significantly over or under
-- their target impression delivery? Pacing issues = revenue risk.

SELECT
    c.campaign_id,
    c.advertiser,
    c.budget,
    c.target_impressions,
    SUM(p.impressions)                         AS actual_impressions,
    ROUND(SUM(p.impressions) * 100.0
          / NULLIF(c.target_impressions, 0), 1) AS delivery_pct,
    CASE
        WHEN SUM(p.impressions) * 100.0
             / NULLIF(c.target_impressions,0) > 110 THEN 'OVER'
        WHEN SUM(p.impressions) * 100.0
             / NULLIF(c.target_impressions,0) < 85  THEN 'UNDER'
        ELSE 'ON_TRACK'
    END                                        AS pacing_status
FROM campaigns c
JOIN daily_performance p ON c.campaign_id = p.campaign_id
GROUP BY c.campaign_id, c.advertiser, c.budget, c.target_impressions
ORDER BY delivery_pct DESC;


-- ── QUERY 6: Device breakdown — CTR and spend share ─────────────────────────
-- Business question: How does campaign performance vary by device?
-- Used to guide CTV vs. mobile vs. desktop inventory pricing strategy.

SELECT
    c.device,
    SUM(p.impressions)                         AS impressions,
    ROUND(SUM(p.spend), 2)                     AS spend,
    ROUND(SUM(p.spend) * 100.0
          / SUM(SUM(p.spend)) OVER (), 2)      AS spend_share_pct,
    ROUND(AVG(p.ctr) * 100, 3)                AS avg_ctr_pct,
    ROUND(AVG(p.completion_rate) * 100, 2)    AS avg_completion_rate_pct,
    ROUND(AVG(p.cpm), 2)                       AS avg_cpm
FROM campaigns c
JOIN daily_performance p ON c.campaign_id = p.campaign_id
GROUP BY c.device
ORDER BY spend DESC;


-- ── QUERY 7: Top 10 content assets by total views ───────────────────────────
-- Business question: Which content drives the most viewership?
-- High-viewership content = premium ad inventory.

SELECT
    ct.content_id,
    ct.title,
    ct.category,
    ct.network,
    SUM(cd.views)                              AS total_views,
    ROUND(AVG(cd.avg_watch_time_min), 2)       AS avg_watch_time_min,
    ROUND(AVG(cd.completion_rate) * 100, 2)    AS avg_completion_rate_pct,
    COUNT(DISTINCT cd.date)                    AS days_active
FROM content ct
JOIN content_daily cd ON ct.content_id = cd.content_id
GROUP BY ct.content_id, ct.title, ct.category, ct.network
ORDER BY total_views DESC
LIMIT 10;


-- ── QUERY 8: Content viewership decay — 1st vs 2nd vs 3rd week ──────────────
-- Business question: How fast does viewership drop off after publish date?
-- Informs how long to run ads against new vs. library content.

SELECT
    ct.category,
    CASE
        WHEN cd.date <= DATE(ct.publish_date, '+7 days')  THEN 'Week 1'
        WHEN cd.date <= DATE(ct.publish_date, '+14 days') THEN 'Week 2'
        WHEN cd.date <= DATE(ct.publish_date, '+21 days') THEN 'Week 3'
        ELSE 'Week 4+'
    END                                        AS content_age_bucket,
    ROUND(AVG(cd.views), 0)                   AS avg_daily_views,
    ROUND(AVG(cd.completion_rate) * 100, 2)   AS avg_completion_rate_pct
FROM content ct
JOIN content_daily cd ON ct.content_id = cd.content_id
GROUP BY ct.category, content_age_bucket
ORDER BY ct.category, content_age_bucket;


-- ── QUERY 9: Regional performance comparison ────────────────────────────────
-- Business question: Which regions over- or under-index on CTR vs.
-- national average? Flags geo-targeting opportunities.

WITH national AS (
    SELECT ROUND(AVG(ctr) * 100, 4) AS national_avg_ctr
    FROM daily_performance
)
SELECT
    c.region,
    SUM(p.impressions)                         AS impressions,
    ROUND(SUM(p.spend), 2)                     AS spend,
    ROUND(AVG(p.ctr) * 100, 4)                AS regional_avg_ctr_pct,
    n.national_avg_ctr,
    ROUND(AVG(p.ctr)*100 - n.national_avg_ctr, 4) AS ctr_vs_national
FROM campaigns c
JOIN daily_performance p ON c.campaign_id = p.campaign_id
CROSS JOIN national n
GROUP BY c.region, n.national_avg_ctr
ORDER BY ctr_vs_national DESC;


-- ── QUERY 10: Frequency & reach efficiency by network ───────────────────────
-- Business question: Which networks are hitting excessive frequency
-- (audience burnout risk) vs. healthy reach/frequency balance?

SELECT
    c.network,
    ROUND(AVG(p.reach), 0)                    AS avg_daily_reach,
    ROUND(AVG(p.frequency), 2)                AS avg_frequency,
    SUM(p.impressions)                        AS total_impressions,
    CASE
        WHEN AVG(p.frequency) > 4.0 THEN 'HIGH_FREQ_RISK'
        WHEN AVG(p.frequency) < 1.5 THEN 'LOW_FREQ'
        ELSE 'HEALTHY'
    END                                       AS frequency_health
FROM campaigns c
JOIN daily_performance p ON c.campaign_id = p.campaign_id
GROUP BY c.network
ORDER BY avg_frequency DESC;


-- ── QUERY 11: Campaigns with zero or anomalous CTR ──────────────────────────
-- Business question: Which campaigns have CTR below 0.1% or above 8%?
-- These are data quality flags — likely tracking issues or tag fires.
-- This is a DATA PRODUCT GAP detection query.

SELECT
    c.campaign_id,
    c.advertiser,
    c.ad_type,
    c.network,
    SUM(p.impressions)            AS impressions,
    SUM(p.clicks)                 AS clicks,
    ROUND(AVG(p.ctr) * 100, 4)  AS avg_ctr_pct,
    CASE
        WHEN AVG(p.ctr) < 0.001 THEN 'ANOMALY: CTR below floor'
        WHEN AVG(p.ctr) > 0.08  THEN 'ANOMALY: CTR above ceiling'
        ELSE 'NORMAL'
    END                          AS ctr_flag
FROM campaigns c
JOIN daily_performance p ON c.campaign_id = p.campaign_id
GROUP BY c.campaign_id, c.advertiser, c.ad_type, c.network
HAVING ctr_flag != 'NORMAL'
ORDER BY avg_ctr_pct DESC;


-- ── QUERY 12: Monthly KPI rollup — executive summary view ───────────────────
-- Business question: One-row-per-month summary for leadership reporting.
-- Core output of the data product this analyst owns.

SELECT
    strftime('%Y-%m', p.date)             AS month,
    COUNT(DISTINCT p.campaign_id)         AS active_campaigns,
    SUM(p.impressions)                    AS impressions,
    SUM(p.clicks)                         AS clicks,
    ROUND(SUM(p.spend), 2)               AS total_spend,
    ROUND(AVG(p.ctr) * 100, 3)          AS avg_ctr_pct,
    ROUND(AVG(p.completion_rate)*100, 2) AS avg_completion_rate_pct,
    ROUND(AVG(p.cpm), 2)                AS avg_cpm,
    SUM(p.reach)                         AS total_reach
FROM daily_performance p
GROUP BY month
ORDER BY month;

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# ── CONFIG ──────────────────────────────────────────────────────────────────
START = datetime(2024, 7, 1)
END   = datetime(2025, 1, 1)
DAYS  = (END - START).days  # 184 days

NETWORKS   = ["StreamMax", "VisionPlus", "PrimeView", "NexGen", "ArcLight"]
CATEGORIES = ["Sports", "News", "Entertainment", "Drama", "Reality", "Documentary"]
DEVICES    = ["CTV", "Mobile", "Desktop", "Tablet"]
REGIONS    = ["Northeast", "Southeast", "Midwest", "West", "Southwest"]
AD_TYPES   = ["Pre-roll", "Mid-roll", "Display", "Sponsored_Content"]
ADVERTISERS = [
    "AutoBrand_A", "CPG_Co_B", "RetailChain_C", "InsureCo_D",
    "TechFirm_E", "BeverageBrand_F", "FinServ_G", "AutoBrand_H"
]

# ── 1. CAMPAIGNS TABLE (150 campaigns) ───────────────────────────────────────
def gen_campaigns(n=150):
    rows = []
    for i in range(1, n+1):
        start_offset = random.randint(0, DAYS - 14)
        duration     = random.choice([7, 14, 21, 28, 42])
        end_offset   = min(start_offset + duration, DAYS)
        budget       = round(random.uniform(25_000, 500_000), -2)
        advertiser   = random.choice(ADVERTISERS)
        ad_type      = random.choice(AD_TYPES)
        network      = random.choice(NETWORKS)
        category     = random.choice(CATEGORIES)
        rows.append({
            "campaign_id":    f"CMP{i:04d}",
            "advertiser":     advertiser,
            "ad_type":        ad_type,
            "network":        network,
            "content_category": category,
            "region":         random.choice(REGIONS),
            "device":         random.choice(DEVICES),
            "budget":         budget,
            "start_date":     (START + timedelta(days=start_offset)).date(),
            "end_date":       (START + timedelta(days=end_offset)).date(),
            "target_impressions": int(budget / random.uniform(0.008, 0.025)),
        })
    return pd.DataFrame(rows)

# ── 2. DAILY CAMPAIGN PERFORMANCE (one row per campaign per day active) ──────
def gen_daily_performance(campaigns):
    rows = []
    for _, c in campaigns.iterrows():
        s = pd.to_datetime(c["start_date"])
        e = pd.to_datetime(c["end_date"])
        active_days = (e - s).days or 1
        # seasonal bump: sports higher on weekends, news higher Mon-Fri
        for d in range(active_days):
            date = s + timedelta(days=d)
            dow  = date.weekday()  # 0=Mon

            base_imps = c["target_impressions"] / active_days
            # add noise + day-of-week pattern
            dow_mult = 1.0
            if c["content_category"] == "Sports" and dow >= 5:
                dow_mult = 1.35
            elif c["content_category"] == "News" and dow < 5:
                dow_mult = 1.2
            elif c["content_category"] == "Reality" and dow >= 4:
                dow_mult = 1.25

            impressions = max(0, int(np.random.normal(base_imps * dow_mult, base_imps * 0.15)))
            ctr         = round(np.random.beta(2, 98) * random.uniform(0.8, 1.4), 4)  # ~1-3%
            clicks      = int(impressions * ctr)
            cpm         = round(random.uniform(6, 32), 2)
            spend       = round(impressions / 1000 * cpm, 2)
            completions = int(impressions * random.uniform(0.55, 0.92))
            comp_rate   = round(completions / impressions, 4) if impressions else 0

            rows.append({
                "campaign_id":       c["campaign_id"],
                "date":              date.date(),
                "impressions":       impressions,
                "clicks":            clicks,
                "ctr":               ctr,
                "spend":             spend,
                "cpm":               cpm,
                "completions":       completions,
                "completion_rate":   comp_rate,
                "reach":             int(impressions * random.uniform(0.55, 0.80)),
                "frequency":         round(random.uniform(1.1, 4.5), 2),
            })
    return pd.DataFrame(rows)

# ── 3. CONTENT PERFORMANCE (content assets, daily) ───────────────────────────
def gen_content(n_assets=80):
    rows = []
    for i in range(1, n_assets+1):
        category  = random.choice(CATEGORIES)
        network   = random.choice(NETWORKS)
        pub_date  = START + timedelta(days=random.randint(0, DAYS-1))
        rows.append({
            "content_id":   f"CNT{i:04d}",
            "title":        f"{category}_Show_{i:03d}",
            "category":     category,
            "network":      network,
            "publish_date": pub_date.date(),
            "episode_length_min": random.choice([22, 44, 60, 90]),
        })
    return pd.DataFrame(rows)

def gen_content_daily(content):
    rows = []
    for _, c in content.iterrows():
        pub = pd.to_datetime(c["publish_date"])
        active_days = (END - pub).days
        if active_days <= 0:
            continue
        # decay curve: high at launch, tails off
        for d in range(min(active_days, 90)):
            date = pub + timedelta(days=d)
            decay = np.exp(-d / 25)
            base_views = random.randint(50_000, 800_000)
            views = max(100, int(np.random.normal(base_views * decay, base_views * decay * 0.2)))
            avg_watch = round(c["episode_length_min"] * random.uniform(0.35, 0.92), 1)
            rows.append({
                "content_id":          c["content_id"],
                "date":                date.date(),
                "views":               views,
                "avg_watch_time_min":  avg_watch,
                "completion_rate":     round(avg_watch / c["episode_length_min"], 4),
                "unique_viewers":      int(views * random.uniform(0.60, 0.92)),
                "device":              random.choice(DEVICES),
                "region":              random.choice(REGIONS),
            })
    return pd.DataFrame(rows)

# ── 4. DASHBOARD USAGE (for A/B test) ────────────────────────────────────────
# Simulates analyst dashboard sessions before/after a UX change (default date
# range switched from 7-day to 30-day on Nov 1 2024)
def gen_dashboard_usage():
    rows = []
    ab_cutoff = datetime(2024, 11, 1)
    users = [f"USER{i:03d}" for i in range(1, 61)]  # 60 analyst users
    for d in range(DAYS):
        date = START + timedelta(days=d)
        group = "post" if date >= ab_cutoff else "pre"
        daily_users = random.sample(users, random.randint(15, 45))
        for u in daily_users:
            # post group: 30-day default → users see more data → longer sessions, more filters
            if group == "post":
                session_len  = round(np.random.normal(8.4, 2.5), 1)
                filters_used = np.random.poisson(3.8)
                exported     = random.random() < 0.38
            else:
                session_len  = round(np.random.normal(5.1, 2.2), 1)
                filters_used = np.random.poisson(2.3)
                exported     = random.random() < 0.21
            rows.append({
                "user_id":          u,
                "date":             date.date(),
                "group":            group,
                "session_length_min": max(0.5, session_len),
                "filters_used":     max(0, filters_used),
                "exported_report":  int(exported),
            })
    return pd.DataFrame(rows)

# ── GENERATE & SAVE ──────────────────────────────────────────────────────────
print("Generating campaigns...")
campaigns = gen_campaigns(150)
campaigns.to_csv("data/campaigns.csv", index=False)

print("Generating daily performance...")
perf = gen_daily_performance(campaigns)
perf.to_csv("data/daily_performance.csv", index=False)

print("Generating content...")
content = gen_content(80)
content.to_csv("data/content.csv", index=False)

print("Generating content daily metrics...")
content_daily = gen_content_daily(content)
content_daily.to_csv("data/content_daily.csv", index=False)

print("Generating dashboard usage (A/B)...")
dash = gen_dashboard_usage()
dash.to_csv("data/dashboard_usage.csv", index=False)

# Summary
print("\n── Dataset Summary ──────────────────")
print(f"campaigns.csv:         {len(campaigns):,} rows")
print(f"daily_performance.csv: {len(perf):,} rows")
print(f"content.csv:           {len(content):,} rows")
print(f"content_daily.csv:     {len(content_daily):,} rows")
print(f"dashboard_usage.csv:   {len(dash):,} rows")
print(f"Total records:         {len(campaigns)+len(perf)+len(content)+len(content_daily)+len(dash):,}")

"""
MoveInSync Play Store ratings report.
Usage:  python ratings_report.py [days]      (default: 30)
Install: pip install google-play-scraper pandas
Compares the last N days with the N days before them.
"""
import sys
from datetime import datetime, timedelta

import pandas as pd
from google_play_scraper import app, reviews, Sort

APP_ID = "com.moveinsync.ets"   # the part after id= in the Play Store URL
DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 30

# Keyword themes (counts are floors: keyword matching misses some reviews
# and includes a few false matches; re-read a sample each run)
THEMES = {
    "Login / OTP":              r"login|log in|logged out|\botp\b|sign in",
    "Crash / slow / not loading": r"\bcrash|\bslow|\blag|not loading|not opening|not open|server down|force close|\bhang|\bstuck",
    "Popups / notifications / permissions": r"notification|policy|disclaimer|permission|pop.?up",
    "ETA / tracking":           r"\beta\b|tracking|real time|live location",
    "No-show / check-in":       r"no.?show|check.?in",
    "QR scan":                  r"\bqr\b|scan",
}


def fetch(days):
    """Fetch reviews newest-first until we pass 2 x days back."""
    cutoff = datetime.now() - timedelta(days=2 * days)
    rows, token = [], None
    while True:
        batch, token = reviews(APP_ID, lang="en", country="in",
                               sort=Sort.NEWEST, count=200,
                               continuation_token=token)
        if not batch:
            break
        rows += batch
        if min(r["at"] for r in batch) < cutoff or token is None:
            break
    df = pd.DataFrame(rows)
    return df[df["at"] >= cutoff] if not df.empty else df


def summarize(df):
    low = df[df["score"] <= 2]
    text = low["content"].fillna("").str.lower()
    out = {
        "reviews": len(df),
        "avg score": round(df["score"].mean(), 2) if len(df) else None,
        "% 1-star": round((df["score"] == 1).mean() * 100, 1) if len(df) else None,
        "low (1-2) reviews": len(low),
    }
    for name, pat in THEMES.items():
        out[name] = int(text.str.contains(pat, regex=True).sum())
    return out


def main():
    info = app(APP_ID, lang="en", country="in")
    print(f"Report date: {datetime.now():%d %b %Y}")
    print(f"Store lifetime score: {info['score']:.2f} "
          f"({info['ratings']:,} ratings) | version {info['version']}\n")

    df = fetch(DAYS)
    split = datetime.now() - timedelta(days=DAYS)
    cur, prev = df[df["at"] >= split], df[df["at"] < split]

    table = pd.DataFrame({f"last {DAYS}d": summarize(cur),
                          f"previous {DAYS}d": summarize(prev)})
    print(table.to_string())
    print("\nTheme counts are keyword floors, not exact totals.")


if __name__ == "__main__":
    main()

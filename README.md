<div align="center">

# 📱 MoveInSync Play Store Ratings Analysis

**Why is the rating lower than it should be, and what should we fix first?**

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-data%20analysis-150458?logo=pandas&logoColor=white)
![Data](https://img.shields.io/badge/data-public%20Play%20Store%20reviews-brightgreen)
![Case](https://img.shields.io/badge/case%20study-Forward%20Deployed%20Engineer-orange)

*Candidate assignment for the MoveInSync Forward Deployed Engineer (Intern to FTE) role*

</div>

---

## 📌 TL;DR

- The employee app shows **4.64★** on the Play Store (114,881 ratings, v12.19.0), but its written reviews tell a different story: **24.2% are 1★**, and the average of the latest 3,000 written reviews is about **3.82**.
- The problem is **chronic, not a recent drop**: monthly averages stay between 3.56 and 4.03, and no single app version explains it.
- About **75% of complaints that give a reason are app problems** (roughly 65-85% given the sample size). The rest are operations (drivers, helpdesk, routing).
- **Fix first:** (1) login / OTP, (2) wrongful no-shows, (3) popup, policy and permission clutter.
- `ratings_report.py` answers *"How are our Play Store ratings?"* in one command, so the question can be asked again and again.

---

## 📊 Key findings

### The rating picture

| Metric | Value |
|---|---|
| Store lifetime score | **4.64★** (114,881 ratings) |
| Written reviews analysed | **3,000** (22 Sep 2025 to 11 Oct 2026) |
| 5★ share of written reviews | 63.8% |
| 1★ share of written reviews | **24.2%** |
| Average of written reviews | ≈ 3.82 |
| Low reviews (1-2★) | 813 (27.1%) |
| Last 30 days vs previous 30 days | 3.76 vs 3.88 (within noise) |

The ratings are **polarised**: a large happy group and a large angry group, with very little in between. The angry group is where the problems are.

### What drives the low ratings

Counts come from keyword matching over all 813 low reviews, so they are **floors, not totals**.

| # | Theme | Real reviews (est.) | What reviewers describe |
|---|---|---|---|
| 1 | 🔐 Login / OTP | ~90 (11%) | OTP not arriving; forced to log in again daily or after 5-10 minutes idle; too many OTPs |
| 2 | 💥 Crash / slow / not loading | ~50 | No single cause: slowness, crashes, load failures, breakage after updates |
| 3 | 🔔 Popups, notifications, permissions | 27 | Policy popup on every launch, repeated delay alerts, forced microphone/location access, an unclosable popup that blocks SOS |
| 4 | 📍 ETA / tracking | 21 | ETA jumps or is far off, location inaccurate, map re-zooms every ~5 seconds |
| 5 | 🚫 No-show / check-in | 23 | 14 of 23 say they were marked no-show unfairly, by drivers (8) or because a scan or cancellation did not register (6) |
| 6 | 📷 QR scan | ~12 | Scanner fails or hangs; reported steadily across 10 app versions |

### App problem or operations problem?

From a random sample of 100 low reviews: **56 app**, **19 operations**, **25 with no usable detail** (this includes 3 reviews whose text contradicts their score).

Of the 75 reviews that give a reason, about **75% are app problems**, so most of what employees complain about is in the product team's control.

---

## ✅ Recommendations

### Do first

| Priority | Fix | Owner | Effort* | First step |
|---|---|---|---|---|
| **1** | **Login / OTP** | App + Backend | Weeks | Keep a refresh token for 15-30 days and do not log out on a brief network drop. Measure OTP delivery rate per SMS provider; add SMS autofill and a resend/fallback channel |
| **2** | **No-show integrity** | App + Ops | Weeks | A successful QR scan or cancellation must clear no-show status at once. Require a logged driver call and a pickup-point location timestamp before a no-show can be marked. Warn the rider before a login no-show auto-cancels the logout trip |
| **3** | **Popup and permission cleanup** | App | Days | Show the transport policy once per policy version. Keep SOS reachable above any popup. Send at most one delay alert per state change. Ask for microphone and location only when a feature needs it |

### Next, in parallel

- **Crash / slow:** pull Play Console Android vitals (crash and ANR rate by version) to find the top 5 causes. This project has review text only, no crash data.
- **QR scan:** add manual code entry beside the scanner and remove the location-accuracy requirement for scanning.
- **ETA / tracking:** log predicted vs actual arrival per trip to measure ETA error; stop the map auto-zooming out while tracking.
- **Operations (hand to transport/vendor teams):** driver behaviour, helpdesk reachability, routing and pickup times.

\*Effort figures are estimates made without access to the codebase.

### How to know it worked

- Login/OTP share of 1-2★ reviews: from ~11% to under 5%.
- 1★ share of written reviews: from ~24% down, tracked monthly with `ratings_report.py`.
- Treat a change as real only if the average moves by more than about 0.15★ or the 1★ share by more than about 4 points at ~230 reviews per window.

---

## 🔁 Run it yourself: the repeatable report

`ratings_report.py` prints the store score, then compares the last *N* days with the *N* days before them: review count, average score, 1★ share, and a count per theme.

```bash
pip install google-play-scraper pandas
# 1. Open ratings_report.py and set APP_ID (the part after id= in the Play Store URL)
python ratings_report.py        # last 30 days vs previous 30
python ratings_report.py 60     # last 60 days vs previous 60
```

Example output (13 Oct 2026):

```
Store lifetime score: 4.64 (114,881 ratings) | version 12.19.0

                                      last 30d  previous 30d
reviews                                 233.00        225.00
avg score                                 3.76          3.88
% 1-star                                 27.50         24.90
low (1-2) reviews                        71.00         60.00
Login / OTP                               7.00          5.00
Crash / slow / not loading                8.00          5.00
Popups / notifications / permissions      6.00          2.00
ETA / tracking                            4.00          0.00
No-show / check-in                        1.00          2.00
QR scan                                   1.00          0.00
```

---

## 🧭 How I got here

| Step | What I did | Result |
|---|---|---|
| 1 | Listed every MoveInSync app on the Play Store | 6 apps; only the **employee app** has enough reviews to analyse (the Driver Partner and Field apps had 7 and 8 written reviews) |
| 2 | Scraped the 3,000 newest written reviews | 22 Sep 2025 to 11 Oct 2026 |
| 3 | Checked the trend by month and by app version | Chronic problem, no single bad release |
| 4 | Read a random sample of 100 low reviews and split app vs operations | ~75% app |
| 5 | Counted keyword themes across all 813 low reviews | Login / OTP is the largest theme |
| 6 | Read the login, crash, no-show, QR, popup and ETA groups and labelled the causes | Root causes per theme (see above) |
| 7 | Scored each theme by size, severity and effort, then ranked | Top 3 fixes |
| 8 | Wrapped the process in a script | `ratings_report.py` |

**Tools:** Python, `google-play-scraper`, `pandas`, and Claude (AI assistant) for guidance, grouping reviews into themes and drafting. I read and labelled samples myself; the larger groups were read with AI assistance.

---

## ⚠️ Assumptions and limitations

- **Written reviews only.** 3,000 reviews against 114,881 lifetime ratings. People who write reviews skew toward extremes, so ~3.82 is lower than the store's 4.64.
- **Keyword counts are floors.** They miss some reviews and include false matches (about 10% for login and about 30% for crash/slow in my samples). Many low reviews just say "worst app" with no reason.
- **Small samples.** Samples of 20-100 reviews carry wide margins (about ±10 to ±20 points), so figures are reported as ranges where it matters.
- **English reviews only.** Hindi and Hinglish reviews are underrepresented.
- **One app.** Only the employee app was analysed.
- **Effort estimates are guesses** made without codebase access.

---

## 📁 Repository structure

```
.
├── README.md                    # this file
├── ratings_report.py            # repeatable 30-day ratings report
├── collect_reviews.py           # scrape reviews to CSV
├── trend_analysis.py            # monthly and per-version trends
├── theme_counts.py              # keyword themes across low reviews
└── MoveInSync_Recommendation.pdf   # the full recommendation
```

---

## 👤 Author

**Gotam Prajapati**
GitHub: [github.com/Wiesslogia](https://github.com/Wiesslogia) | LinkedIn: [linkedin.com/in/gotamPrajapati](https://linkedin.com/in/gotamPrajapati)

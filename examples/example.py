"""Demo: every chart in simple_eda, rendered to a single gallery PNG."""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import simple_eda as cv

cv.set_theme()
rng = np.random.default_rng(7)

months = pd.Index(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], name="month")
trend = pd.DataFrame({
    "signups": [120, 145, 138, 172, 205, 243],
    "active": [90, 110, 121, 140, 165, 190],
}, index=months)

channels = pd.DataFrame({
    "email": [340, 290, 410],
    "social": [220, 300, 260],
}, index=pd.Index(["Q1", "Q2", "Q3"], name="quarter"))

ranked = pd.Series([48, 39, 31, 22, 14],
                   index=["Search", "Direct", "Referral", "Social", "Email"],
                   name="visits")

points = pd.DataFrame({
    "spend": rng.uniform(10, 100, 90),
    "revenue": rng.uniform(20, 200, 90),
    "region": rng.choice(["North", "South", "West"], 90),
})

durations = pd.Series(rng.normal(45, 12, 500), name="session (min)")

fig, axes = plt.subplots(2, 3, figsize=(16, 9))
cv.line(trend, title="Growth over time", ax=axes[0, 0])
cv.bar(channels, title="Channel volume by quarter", ax=axes[0, 1])
cv.barh(ranked, title="Traffic sources", ax=axes[0, 2])
cv.scatter(points, "spend", "revenue", color="region",
           title="Spend vs revenue", ax=axes[1, 0])
cv.hist(durations, title="Session durations", ax=axes[1, 1])
cv.line(trend["signups"], title="Single series (no legend)", ax=axes[1, 2])

fig.set_facecolor("#fcfcfb")
fig.tight_layout(pad=2.0)
out = os.path.join(os.path.dirname(__file__), "gallery.png")
fig.savefig(out, dpi=120, bbox_inches="tight")
print(f"wrote {out}")

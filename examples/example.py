"""Demo: simple_eda on the Palmer Penguins dataset, rendered to one gallery PNG.

Shows off the three signature charts (ridgeline, lollipop, dumbbell) alongside
scatter and hist, all driven straight from a DataFrame.
Data: examples/penguins.csv (Palmer Penguins; Horst, Hill & Gorman, 2020).
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

import simple_eda as cv

HERE = os.path.dirname(__file__)
cv.set_theme()

penguins = pd.read_csv(os.path.join(HERE, "penguins.csv"))

# --- shape a few tidy tables straight from the raw frame -------------------

# number of penguins per species → ranked lollipop
species_counts = penguins.groupby("species").size()

# mean body mass by sex per species → dumbbell (female vs male)
sexed = penguins.dropna(subset=["sex"])
mass_by_sex = (sexed.groupby(["species", "sex"])["body_mass_g"]
               .mean().unstack())[["FEMALE", "MALE"]]
mass_by_sex.columns = ["Female", "Male"]   # tidy legend labels

# --- draw the gallery (3 charts on top, 2 centred below) -------------------

fig = plt.figure(figsize=(16, 9))
gs = fig.add_gridspec(2, 6)
ax_ridge = fig.add_subplot(gs[0, 0:2])
ax_lolli = fig.add_subplot(gs[0, 2:4])
ax_dumb = fig.add_subplot(gs[0, 4:6])
ax_scat = fig.add_subplot(gs[1, 1:3])
ax_hist = fig.add_subplot(gs[1, 3:5])

cv.ridgeline(penguins, value="body_mass_g", group="species",
             center="mean", band="sd",
             title="Body mass distribution by species",
             xlabel="body mass (g)", ax=ax_ridge)
cv.lollipop(species_counts, title="Number of penguins by species",
            xlabel="count", ax=ax_lolli)
cv.dumbbell(mass_by_sex, title="Body mass: female vs male",
            xlabel="body mass (g)", ax=ax_dumb)
sc = cv.scatter(penguins, "bill_length_mm", "bill_depth_mm", color="species",
                trend=True, alpha=0.45, title="Bill length vs bill depth",
                ax=ax_scat)
sc.set_xlabel("bill length (mm)")
sc.set_ylabel("bill depth (mm)")
cv.hist(penguins, "flipper_length_mm", by="species",
        title="Flipper length by species",
        xlabel="flipper length (mm)", ax=ax_hist)

for a in (ax_ridge, ax_lolli, ax_dumb, ax_scat, ax_hist):
    a.grid(False)                    # strip every gridline
for a in (ax_lolli, ax_dumb):        # faint x-grid back on the magnitude charts
    a.set_axisbelow(True)
    a.grid(axis="x", visible=True, color="#e7e6e0", linewidth=0.8)

fig.set_facecolor("#fcfcfb")
fig.tight_layout(pad=2.0)
out = os.path.join(HERE, "gallery.png")
fig.savefig(out, dpi=120, bbox_inches="tight")
print(f"wrote {out}")

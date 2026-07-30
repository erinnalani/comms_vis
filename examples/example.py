"""Demo: simple_eda on the Palmer Penguins dataset, rendered to one gallery PNG.

Shows off the three signature charts (ridgeline, lollipop, dumbbell) alongside
the everyday ones (scatter, hist, bar), all driven straight from a DataFrame.
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

# mean flipper length per species → ranked lollipop
flipper = penguins.groupby("species")["flipper_length_mm"].mean()

# mean body mass by sex per species → dumbbell (female vs male)
sexed = penguins.dropna(subset=["sex"])
mass_by_sex = (sexed.groupby(["species", "sex"])["body_mass_g"]
               .mean().unstack())[["FEMALE", "MALE"]]

# species counts per island → grouped bars
counts = (penguins.groupby(["island", "species"]).size()
          .unstack(fill_value=0))

# --- draw the gallery ------------------------------------------------------

fig, axes = plt.subplots(2, 3, figsize=(16, 9))

cv.ridgeline(penguins, value="body_mass_g", group="species",
             title="Body mass distribution by species",
             xlabel="body mass (g)", ax=axes[0, 0])
cv.lollipop(flipper, title="Mean flipper length by species",
            xlabel="flipper length (mm)", ax=axes[0, 1])
cv.dumbbell(mass_by_sex, title="Body mass: female vs male",
            xlabel="body mass (g)", ax=axes[0, 2])
sc = cv.scatter(penguins, "bill_length_mm", "bill_depth_mm", color="species",
                title="Bill length vs bill depth", ax=axes[1, 0])
sc.set_xlabel("bill length (mm)")
sc.set_ylabel("bill depth (mm)")
cv.hist(penguins, "bill_length_mm", by="species", title="Bill length by species",
        xlabel="bill length (mm)", ax=axes[1, 1])
cv.bar(counts, title="Penguins per island", ax=axes[1, 2])

fig.set_facecolor("#fcfcfb")
fig.tight_layout(pad=2.0)
out = os.path.join(HERE, "gallery.png")
fig.savefig(out, dpi=120, bbox_inches="tight")
print(f"wrote {out}")

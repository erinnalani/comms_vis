"""Demo: simple_eda on the Palmer Penguins dataset, rendered to one gallery PNG.

A small "poster" built from a single DataFrame: a body-mass ridgeline, a
species-count lollipop, a female-vs-male dumbbell, a bill-length-vs-depth
scatter, a flipper-length histogram, and a penguin trio that doubles as the
species key. Species keep one consistent colour throughout; sex gets its own
coastal pair on the dumbbell.

Data: examples/penguins.csv (Palmer Penguins; Horst, Hill & Gorman, 2020).
Penguin art: examples/{adelie,chinstrap,gentoo}.png.
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
import pandas as pd
from PIL import Image

import simple_eda as cv

HERE = os.path.dirname(__file__)
cv.set_theme()

SPCOL = {"Adelie": cv.PALETTE[0], "Chinstrap": cv.PALETTE[1], "Gentoo": cv.PALETTE[2]}
FEM, MAL = "#999933", "#0077BB"        # coastal sex colours (olive / blue)
INK, SURFACE = "#0b0b0b", "#fcfcfb"

penguins = pd.read_csv(os.path.join(HERE, "penguins.csv"))
species_counts = penguins.groupby("species").size()
sexed = penguins.dropna(subset=["sex"])
mass_by_sex = (sexed.groupby(["species", "sex"])["body_mass_g"]
               .mean().unstack())[["FEMALE", "MALE"]]
mass_by_sex.columns = ["Female", "Male"]


def penguin_trio(order, height=420, gap=80):
    """Baseline-aligned strip of the species PNGs; returns (rgba, w, h, centres)."""
    parts = []
    for name in order:
        im = Image.open(os.path.join(HERE, f"{name}.png")).convert("RGBA")
        im = im.crop(im.getbbox())
        w, h = im.size
        parts.append(im.resize((max(1, int(w * height / h)), height)))
    total = sum(p.size[0] for p in parts) + gap * (len(parts) - 1)
    strip = Image.new("RGBA", (total, height), (0, 0, 0, 0))
    centres, x = [], 0
    for p in parts:
        strip.alpha_composite(p, (x, 0))
        centres.append(x + p.size[0] / 2)
        x += p.size[0] + gap
    return np.asarray(strip), total, height, centres


ORDER = ["chinstrap", "gentoo", "adelie"]
strip, strip_w, strip_h, centres = penguin_trio(ORDER)

# --- draw the gallery (2x3) ------------------------------------------------
fig = plt.figure(figsize=(16, 9))
gs = fig.add_gridspec(2, 3, hspace=0.40, wspace=0.26)
axR = fig.add_subplot(gs[0, 0])
axL = fig.add_subplot(gs[0, 1])
axD = fig.add_subplot(gs[0, 2])
axS = fig.add_subplot(gs[1, 0])
axH = fig.add_subplot(gs[1, 1])
axP = fig.add_subplot(gs[1, 2])

cv.ridgeline(penguins, value="body_mass_g", group="species", center="mean",
             band="sd", title="Body mass distribution", xlabel="body mass (g)",
             ax=axR)

cv.lollipop(species_counts, colors=SPCOL, title="Number of penguins",
            xlabel="count", ax=axL)

cv.dumbbell(mass_by_sex, colors=(FEM, MAL), title="Body mass: female vs male",
            xlabel="body mass (g)", ax=axD)
ranked = mass_by_sex.sort_values("Female")          # matches dumbbell's own order
for i, (_, row) in enumerate(ranked.iterrows()):
    pct = (row["Male"] - row["Female"]) / row["Female"] * 100
    axD.annotate(f"+{pct:.0f}%", ((row["Female"] + row["Male"]) / 2, i),
                 xytext=(0, 7), textcoords="offset points", ha="center",
                 va="bottom", fontsize=9, fontweight="bold", color=INK)
axD.set_ylim(-0.5, len(ranked) - 1 + 0.55)
axD.legend(loc="lower right")

sc = cv.scatter(penguins, "bill_length_mm", "bill_depth_mm", color="species",
                trend=True, alpha=0.45, title="Bill length vs bill depth", ax=axS)
sc.set_xlabel("bill length (mm)")
sc.set_ylabel("bill depth (mm)")
if sc.get_legend():
    sc.get_legend().remove()      # direct labels instead, so the panel stands alone
for sp, (lx, ly) in {"Adelie": (35, 19.7), "Chinstrap": (52.5, 19.6),
                     "Gentoo": (52.5, 14.1)}.items():
    sc.text(lx, ly, sp, color=SPCOL[sp], fontsize=12.5, fontweight="bold",
            ha="center", path_effects=[pe.withStroke(linewidth=3.5, foreground=SURFACE)])

cv.hist(penguins, "flipper_length_mm", by="species",
        title="Flipper length by species", xlabel="flipper length (mm)", ax=axH)
if axH.get_legend():
    axH.get_legend().remove()

for a in (axR, axL, axD, axS, axH):
    a.grid(False)
for a in (axL, axD):                       # faint x-grid aids value reading
    a.set_axisbelow(True)
    a.grid(axis="x", visible=True, color="#e7e6e0", linewidth=0.8)

# penguin trio (bottom-right), doubling as the species key, centred in its cell
axP.axis("off")
axP.imshow(strip, extent=[0, strip_w, 0, strip_h], aspect="equal",
           interpolation="antialiased")
cell = gs[1, 2].get_position(fig)
cell_aspect = (cell.width * 16) / (cell.height * 9)
pad_x, y_lo, y_hi = 60, -120, strip_h
box_w, box_h = strip_w + 2 * pad_x, strip_h - y_lo
if box_w / box_h >= cell_aspect:           # fit, then centre — never overflow
    x_range, y_range = box_w, box_w / cell_aspect
else:
    x_range, y_range = box_h * cell_aspect, box_h
mid_x, mid_y = strip_w / 2, (y_lo + y_hi) / 2
axP.set_xlim(mid_x - x_range / 2, mid_x + x_range / 2)
axP.set_ylim(mid_y - y_range / 2, mid_y + y_range / 2)
axP.set_aspect("equal", adjustable="box")
for name, ctr in zip(ORDER, centres):
    axP.text(ctr, -30, name.capitalize(), ha="center", va="top", fontsize=12.5,
             fontweight="bold", color=SPCOL[name.capitalize()])

fig.set_facecolor("#fcfcfb")
out = os.path.join(HERE, "gallery.png")
fig.savefig(out, dpi=120, bbox_inches="tight")
print(f"wrote {out}")

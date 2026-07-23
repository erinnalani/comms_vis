# comms_vis

A tiny, modern charting library built on **matplotlib** and **pandas** — nothing
else. One file, under 200 lines. It gives you clean, colorblind-safe charts
straight from a DataFrame without the usual matplotlib boilerplate.

![gallery](gallery.png)

## Why

Default matplotlib looks dated and takes a dozen lines to tidy up. `comms_vis`
applies a modern theme (no chartjunk, hairline gridlines, a validated
categorical palette) and gives you five chart functions that each take a pandas
object and return the `Axes` for further tweaking.

## Install

Just needs matplotlib and pandas:

```bash
pip install matplotlib pandas
```

Then drop `comms_vis.py` next to your code.

## Usage

```python
import pandas as pd
import comms_vis as cv

cv.set_theme()   # call once to apply the modern look

df = pd.DataFrame(
    {"signups": [120, 145, 138, 172], "active": [90, 110, 121, 140]},
    index=["Jan", "Feb", "Mar", "Apr"],
)

ax = cv.line(df, title="Growth over time")
ax.figure.savefig("growth.png")
```

## Functions

Every function returns a matplotlib `Axes`. Pass `ax=` to draw into an existing
subplot. A legend is added automatically only when there is more than one series.

| Function | Purpose | Input |
|----------|---------|-------|
| `set_theme()` | Apply the modern default style globally | — |
| `line(data, ...)` | Line chart; one line per column | DataFrame / Series |
| `bar(data, ...)` | Grouped vertical bars | DataFrame / Series |
| `barh(data, ...)` | Ranked horizontal bars | DataFrame / Series |
| `scatter(data, x, y, color=None, ...)` | Scatter, optionally split by a category | DataFrame |
| `hist(data, column=None, bins=20, ...)` | Distribution of one numeric column | DataFrame / Series |

Common keyword args: `title`, `xlabel`, `ylabel`, `ax`.

`PALETTE` is the exported list of eight colorblind-safe hues, assigned to series
in order.

## Example

Run the full gallery shown above:

```bash
python example.py   # writes gallery.png
```

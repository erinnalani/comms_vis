# simple-eda

A tiny, modern charting library built on **matplotlib** and **pandas** — nothing
else. The core is a single ~157-line module with a colorblind-safe palette and
clean, chartjunk-free defaults. It gives you five chart helpers straight from a
DataFrame without the usual matplotlib boilerplate.

![gallery](examples/gallery.png)

## Why

Default matplotlib looks dated and takes a dozen lines to tidy up. `simple_eda`
applies a modern theme (no chartjunk, hairline gridlines, a validated
categorical palette) and gives you chart functions that each take a pandas
object and return the `Axes` for further tweaking.

## Layout

```
simple-eda-project/
├── src/
│   └── simple_eda/
│       ├── __init__.py      # public API
│       └── core.py          # the chart functions + theme
├── examples/
│   ├── example.py           # renders the gallery above
│   └── gallery.png
├── README.md
├── pyproject.toml
└── LICENSE
```

## Install

```bash
pip install -e .          # from the project root
```

This pulls in matplotlib and pandas.

## Usage

```python
import pandas as pd
import simple_eda as se

se.set_theme()   # call once to apply the modern look

df = pd.DataFrame(
    {"signups": [120, 145, 138, 172], "active": [90, 110, 121, 140]},
    index=["Jan", "Feb", "Mar", "Apr"],
)

ax = se.line(df, title="Growth over time")
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
python examples/example.py   # writes examples/gallery.png
```

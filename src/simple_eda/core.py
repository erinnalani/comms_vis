"""simple_eda.core — a tiny, modern matplotlib + pandas charting library.

Design goals: clean marks, recessive chrome, a colorblind-safe categorical
palette, and a legend whenever more than one series is drawn. Every function
takes a pandas DataFrame/Series and returns the matplotlib ``Axes`` so you can
keep customizing.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np  # ships with pandas; no new dependency
import pandas as pd

__all__ = ["set_theme", "PALETTE", "line", "bar", "barh", "scatter", "hist",
           "lollipop", "dumbbell", "ridgeline"]

# Categorical palette (assigned in fixed order). The first three — tan, light
# blue, teal — carry most charts; the rest are Paul Tol's "muted" hues as
# colorblind-safe fallbacks for higher series counts.
PALETTE = ["#C9A66B", "#88CCEE", "#44AA99",           # tan, light blue, teal
           "#CC6677", "#332288", "#DDCC77", "#117733",  # rose, indigo, sand, green
           "#882255", "#999933", "#AA4499"]             # wine, olive, purple

_INK = "#0b0b0b"          # primary text
_MUTED = "#898781"        # axis labels / ticks
_GRID = "#e1e0d9"         # hairline gridlines
_BASELINE = "#c3c2b7"     # axis baseline
_SURFACE = "#fcfcfb"      # chart surface


def set_theme() -> None:
    """Apply the modern default look to all subsequent matplotlib figures."""
    plt.rcParams.update({
        "figure.facecolor": _SURFACE,
        "axes.facecolor": _SURFACE,
        "axes.edgecolor": _BASELINE,
        "axes.linewidth": 1.0,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.titlecolor": _INK,
        "axes.titlelocation": "left",
        "axes.titlepad": 14,
        "axes.labelsize": 11,
        "axes.labelcolor": _MUTED,
        "axes.prop_cycle": plt.cycler(color=PALETTE),
        "grid.color": _GRID,
        "grid.linewidth": 1.0,
        "text.color": _INK,
        "xtick.color": _MUTED,
        "ytick.color": _MUTED,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "xtick.bottom": False,
        "ytick.left": False,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 11,
        "figure.dpi": 110,
        "figure.autolayout": True,
        "legend.frameon": False,
        "legend.fontsize": 10,
    })


def _new_ax(ax, figsize=(8, 5)):
    if ax is None:
        _, ax = plt.subplots(figsize=figsize)
    return ax


def _finish(ax, title, xlabel, ylabel, legend):
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if legend:
        ax.legend()
    return ax


def _as_frame(data):
    """Coerce a Series to a one-column DataFrame; leave DataFrames as-is."""
    if isinstance(data, pd.Series):
        return data.to_frame()
    return data


def line(data, title=None, xlabel=None, ylabel=None, ax=None):
    """Line chart. Each column of ``data`` becomes one series."""
    df = _as_frame(data)
    ax = _new_ax(ax)
    for col in df.columns:
        ax.plot(df.index, df[col], linewidth=2.0, label=str(col),
                solid_capstyle="round", solid_joinstyle="round")
    return _finish(ax, title, xlabel, ylabel, legend=df.shape[1] > 1)


def bar(data, title=None, xlabel=None, ylabel=None, ax=None):
    """Vertical bar chart. Multiple columns are drawn grouped side by side."""
    df = _as_frame(data)
    ax = _new_ax(ax)
    n, x = df.shape[1], range(len(df.index))
    width = 0.8 / n
    for i, col in enumerate(df.columns):
        offset = (i - (n - 1) / 2) * width
        ax.bar([p + offset for p in x], df[col], width=width * 0.92,
               label=str(col), color=PALETTE[i % len(PALETTE)])
    ax.set_xticks(list(x))
    ax.set_xticklabels([str(v) for v in df.index])
    return _finish(ax, title, xlabel, ylabel, legend=n > 1)


def barh(data, title=None, xlabel=None, ylabel=None, ax=None):
    """Horizontal bar chart — best for ranked categories with long labels."""
    df = _as_frame(data)
    ax = _new_ax(ax)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    n, y = df.shape[1], range(len(df.index))
    height = 0.8 / n
    for i, col in enumerate(df.columns):
        offset = (i - (n - 1) / 2) * height
        ax.barh([p + offset for p in y], df[col], height=height * 0.92,
                label=str(col), color=PALETTE[i % len(PALETTE)])
    ax.set_yticks(list(y))
    ax.set_yticklabels([str(v) for v in df.index])
    ax.invert_yaxis()
    return _finish(ax, title, xlabel, ylabel, legend=n > 1)


def _trend_line(ax, xv, yv, color):
    """Draw a straight OLS best-fit line for ``xv`` vs ``yv`` onto ``ax``."""
    pair = pd.DataFrame({"x": xv, "y": yv}).dropna()
    if len(pair) < 2:
        return
    slope, intercept = np.polyfit(pair["x"], pair["y"], 1)
    xs = np.array([pair["x"].min(), pair["x"].max()])
    ax.plot(xs, slope * xs + intercept, color=color, linewidth=2.2,
            solid_capstyle="round", zorder=3)


def scatter(data, x, y, color=None, trend=False, title=None, ax=None):
    """Scatter plot of columns ``x`` vs ``y``, optionally split by ``color``.

    Set ``trend=True`` to overlay a straight (OLS) line of best fit. When the
    points are split by ``color``, one line is drawn per group in the group's
    colour — which is the honest choice for grouped data, since a single line
    across all groups can point the opposite way to every group within it.
    """
    ax = _new_ax(ax)
    if color:
        for i, (key, grp) in enumerate(data.groupby(color)):
            c = PALETTE[i % len(PALETTE)]
            ax.scatter(grp[x], grp[y], s=42, label=str(key), alpha=0.85,
                       edgecolor=_SURFACE, linewidth=0.8, color=c)
            if trend:
                _trend_line(ax, grp[x], grp[y], c)
    else:
        ax.scatter(data[x], data[y], s=42, alpha=0.85,
                   edgecolor=_SURFACE, linewidth=0.8, color=PALETTE[0])
        if trend:
            _trend_line(ax, data[x], data[y], PALETTE[0])
    return _finish(ax, title, x, y, legend=bool(color))


def hist(data, column=None, by=None, bins=20, title=None, xlabel=None, ax=None):
    """Histogram of a single numeric column (or a Series).

    Pass ``by`` (a categorical column name) to split the distribution into one
    translucent, overlaid histogram per group — sharing a single set of bin
    edges — so the overlap between groups is visible. Requires a DataFrame and
    a ``column`` when ``by`` is given.
    """
    ax = _new_ax(ax)
    if by is not None:
        edges = np.histogram_bin_edges(data[column].dropna(), bins=bins)
        for i, (key, grp) in enumerate(data.groupby(by)):
            ax.hist(grp[column].dropna(), bins=edges, label=str(key),
                    color=PALETTE[i % len(PALETTE)], alpha=0.6,
                    edgecolor=_SURFACE, linewidth=0.6)
        ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
        return _finish(ax, title, xlabel or column, "count", legend=True)

    values = data if isinstance(data, pd.Series) else data[column]
    ax.hist(values.dropna(), bins=bins, color=PALETTE[0],
            edgecolor=_SURFACE, linewidth=0.8)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    return _finish(ax, title, xlabel or (column or values.name), "count",
                   legend=False)


def _one_column(data):
    """Return a (labels, values) pair from a Series or one-column DataFrame."""
    if isinstance(data, pd.DataFrame):
        if data.shape[1] != 1:
            raise ValueError("expected a Series or a one-column DataFrame")
        s = data.iloc[:, 0]
    else:
        s = data
    return s.index, s


def lollipop(data, title=None, xlabel=None, ylabel=None, sort=True, ax=None):
    """Ranked lollipop chart — a lighter, cleaner alternative to ``barh``.

    A thin stem runs from the baseline to a dot at each category's value.
    Accepts a Series or a one-column DataFrame; values are sorted descending
    by default so the ranking reads top-to-bottom.
    """
    _, s = _one_column(data)
    if sort:
        s = s.sort_values(ascending=True)   # ascending → largest on top after invert
    else:
        s = s[::-1]
    ax = _new_ax(ax)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    y = range(len(s))
    ax.hlines(list(y), 0, s.values, color=_BASELINE, linewidth=2.0, zorder=1)
    ax.scatter(s.values, list(y), s=90, color=PALETTE[0], zorder=2,
               edgecolor=_SURFACE, linewidth=1.2)
    ax.set_yticks(list(y))
    ax.set_yticklabels([str(v) for v in s.index])
    ax.margins(x=0.08)
    return _finish(ax, title, xlabel, ylabel, legend=False)


def dumbbell(data, title=None, xlabel=None, ylabel=None, sort=True, ax=None):
    """Dumbbell chart — two dots per category joined by a connector.

    Ideal for a before/after or A-vs-B comparison across categories (e.g.
    male vs female). ``data`` must be a DataFrame with exactly two numeric
    columns; each column becomes one dot colour, labelled in the legend.
    Rows are sorted by the first column by default.
    """
    df = _as_frame(data)
    if df.shape[1] != 2:
        raise ValueError("dumbbell expects a DataFrame with exactly two columns")
    if sort:
        df = df.sort_values(df.columns[0], ascending=True)
    else:
        df = df[::-1]
    a, b = df.columns[0], df.columns[1]
    ax = _new_ax(ax)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    y = list(range(len(df)))
    ax.hlines(y, df[a].values, df[b].values, color=_BASELINE, linewidth=2.5,
              zorder=1)
    ax.scatter(df[a].values, y, s=90, color=PALETTE[0], label=str(a), zorder=2,
               edgecolor=_SURFACE, linewidth=1.2)
    ax.scatter(df[b].values, y, s=90, color=PALETTE[1], label=str(b), zorder=2,
               edgecolor=_SURFACE, linewidth=1.2)
    ax.set_yticks(y)
    ax.set_yticklabels([str(v) for v in df.index])
    ax.margins(x=0.08)
    return _finish(ax, title, xlabel, ylabel, legend=True)


def _kde(x, grid):
    """Gaussian KDE on ``grid`` using Silverman's rule for bandwidth."""
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    n = x.size
    if n < 2:
        return np.zeros_like(grid)
    std = x.std(ddof=1)
    iqr = np.subtract(*np.percentile(x, [75, 25]))
    spread = min(std, iqr / 1.349) if iqr > 0 else std
    bw = 0.9 * spread * n ** (-0.2) or 1.0
    u = (grid[:, None] - x[None, :]) / bw
    return np.exp(-0.5 * u ** 2).sum(axis=1) / (n * bw * np.sqrt(2 * np.pi))


def ridgeline(data, value, group, title=None, xlabel=None, overlap=1.3,
              ax=None):
    """Ridgeline plot — one smoothed distribution per group, gently overlapped.

    Great for comparing the *shape* of a numeric variable across categories.
    ``value`` is the numeric column and ``group`` the categorical column.
    Groups are ordered by their median so the ridges climb; ``overlap`` sets
    how far adjacent ridges intrude on each other (1.0 = just touching).
    """
    vals = data[value].astype(float)
    order = (data.groupby(group)[value].median().sort_values().index.tolist())
    lo, hi = np.nanmin(vals), np.nanmax(vals)
    pad = 0.05 * (hi - lo)
    grid = np.linspace(lo - pad, hi + pad, 512)

    densities = {g: _kde(data.loc[data[group] == g, value].values, grid)
                 for g in order}
    peak = max((d.max() for d in densities.values()), default=1.0) or 1.0
    scale = overlap / peak

    ax = _new_ax(ax, figsize=(8, 0.9 * len(order) + 2))
    ax.grid(visible=False)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([str(g) for g in order])
    # Draw back-to-front so lower ridges overlap those behind them.
    for i in reversed(range(len(order))):
        g = order[i]
        curve = i + densities[g] * scale
        color = PALETTE[i % len(PALETTE)]
        ax.fill_between(grid, i, curve, color=color, alpha=0.75, zorder=i,
                        linewidth=0)
        ax.plot(grid, curve, color=_SURFACE, linewidth=1.4, zorder=i)
    ax.set_ylim(-0.2, len(order) - 1 + overlap + 0.3)
    ax.margins(x=0)
    return _finish(ax, title, xlabel or value, None, legend=False)

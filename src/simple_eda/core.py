"""simple_eda.core — a tiny, modern matplotlib + pandas charting library.

Design goals: clean marks, recessive chrome, a colorblind-safe categorical
palette, and a legend whenever more than one series is drawn. Every function
takes a pandas DataFrame/Series and returns the matplotlib ``Axes`` so you can
keep customizing.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

__all__ = ["set_theme", "PALETTE", "line", "bar", "barh", "scatter", "hist"]

# Validated, colorblind-safe categorical palette (assigned in fixed order).
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
           "#e87ba4", "#008300", "#4a3aa7", "#e34948"]

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


def scatter(data, x, y, color=None, title=None, ax=None):
    """Scatter plot of columns ``x`` vs ``y``, optionally split by ``color``."""
    ax = _new_ax(ax)
    if color:
        for i, (key, grp) in enumerate(data.groupby(color)):
            ax.scatter(grp[x], grp[y], s=42, label=str(key), alpha=0.85,
                       edgecolor=_SURFACE, linewidth=0.8,
                       color=PALETTE[i % len(PALETTE)])
    else:
        ax.scatter(data[x], data[y], s=42, alpha=0.85,
                   edgecolor=_SURFACE, linewidth=0.8, color=PALETTE[0])
    return _finish(ax, title, x, y, legend=bool(color))


def hist(data, column=None, bins=20, title=None, xlabel=None, ax=None):
    """Histogram of a single numeric column (or a Series)."""
    values = data if isinstance(data, pd.Series) else data[column]
    ax = _new_ax(ax)
    ax.hist(values.dropna(), bins=bins, color=PALETTE[0],
            edgecolor=_SURFACE, linewidth=0.8)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    return _finish(ax, title, xlabel or (column or values.name), "count",
                   legend=False)

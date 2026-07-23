"""simple_eda — a tiny, modern matplotlib + pandas charting library.

Import the whole toolkit and start plotting straight from a pandas object:

    import simple_eda as se

    se.set_theme()
    se.line(df, title="Growth over time")
"""

from .core import (
    PALETTE,
    set_theme,
    line,
    bar,
    barh,
    scatter,
    hist,
)

__version__ = "0.1.0"

__all__ = [
    "PALETTE",
    "set_theme",
    "line",
    "bar",
    "barh",
    "scatter",
    "hist",
]

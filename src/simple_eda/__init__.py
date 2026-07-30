"""simple_eda — a tiny, modern matplotlib + pandas charting library.

Import the whole toolkit and start plotting straight from a pandas object:

    import simple_eda as se

    se.set_theme()
    se.scatter(df, "x", "y", color="group", title="X vs Y")
"""

from .core import (
    PALETTE,
    set_theme,
    scatter,
    hist,
    lollipop,
    dumbbell,
    ridgeline,
)

__version__ = "0.2.0"

__all__ = [
    "PALETTE",
    "set_theme",
    "scatter",
    "hist",
    "lollipop",
    "dumbbell",
    "ridgeline",
]

"""Shared utility functions."""

from __future__ import annotations

import os
import sys


def resource_path(relative_path: str) -> str:
    """Resolve *relative_path* inside a PyInstaller bundle or the project root."""
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def interpolate_color(color: str, factor: float) -> str:
    """Interpolate a hex color toward black by *factor* (0.0 = full color, 1.0 = black).

    Args:
        color: Hex color string in format ``#RRGGBB``.
        factor: Blend factor where 0 returns the original color and 1 returns black.

    Returns:
        Interpolated hex color string.
    """
    r = int(int(color[1:3], 16) * (1.0 - factor))
    g = int(int(color[3:5], 16) * (1.0 - factor))
    b = int(int(color[5:7], 16) * (1.0 - factor))
    return f"#{r:02x}{g:02x}{b:02x}"

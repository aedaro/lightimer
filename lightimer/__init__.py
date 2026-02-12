"""Lightimer — a lightweight countdown timer for presentations."""

from lightimer.config import (
    INIT_DURATION_S,
    REFRESH_CYCLE_MS,
    BG_COLOR,
    LEVEL_COLOR,
    TIME_COLOR,
    TIME_FONT,
)
from lightimer.timer import StaticTimer
from lightimer.sound import play_notification
from lightimer.ui import LightimerApp

__all__ = [
    "LightimerApp",
    "StaticTimer",
    "play_notification",
    "INIT_DURATION_S",
    "REFRESH_CYCLE_MS",
    "BG_COLOR",
    "LEVEL_COLOR",
    "TIME_COLOR",
    "TIME_FONT",
]

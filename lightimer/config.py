"""Application-wide constants and configuration."""

from enum import Enum, auto

# ── Window dimensions ────────────────────────────────────────────────
HEIGHT_V: int = 800
WIDTH_V: int = 116
HEIGHT_H: int = 50
WIDTH_H: int = 1000

# ── Gaps / margins ───────────────────────────────────────────────────
WIN_GAP: int = 25
LIN_GAP: int = 20

# ── Colour ───────────────────────────────────────────────────────────
RGB_MAX: int = 255
BG_COLOR: str = "#000000"
LEVEL_COLOR: str = "#00FF00"
TIME_COLOR: str = "#777777"

# ── Timing ───────────────────────────────────────────────────────────
INIT_DURATION_S: int = 300  # 5 minutes
REFRESH_CYCLE_MS: int = 8  # ~120 fps

# ── Font ─────────────────────────────────────────────────────────────
TIME_FONT: tuple[str, int] = ("Helvetica", 24)

# ── Resource paths (relative to bundle / project root) ───────────────
SOUND_PATH: str = "sound/timesup.wav"
ICON_PATH: str = "icon/lightimer.gif"


class Orientation(Enum):
    """Timer bar orientation."""

    VERTICAL = auto()
    HORIZONTAL = auto()

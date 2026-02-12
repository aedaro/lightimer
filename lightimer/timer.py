"""Countdown timer with start / stop / reset semantics."""

from __future__ import annotations

import logging
import time

logger = logging.getLogger(__name__)


class StaticTimer:
    """A simple wall-clock countdown timer.

    The timer measures elapsed/remaining time by capturing a timestamp at
    ``start()`` and computing deltas on the fly — no background thread needed.
    """

    def __init__(self, period: float) -> None:
        self.set(period)

    # ── public API ────────────────────────────────────────────────────

    def set(self, period: float) -> None:
        """Set a new countdown *period* (seconds) and reset."""
        self._period: float = period
        self.reset()

    def reset(self) -> None:
        """Reset the timer to the full period without starting it."""
        self._remaining: float = self._period
        self._timestamp: float = 0.0
        self.is_running: bool = False

    def start(self) -> None:
        """Start (or resume) the countdown."""
        logger.debug("timer start: %.2fs remaining", self.get_remaining())
        self._timestamp = time.time()
        self.is_running = True

    def stop(self) -> None:
        """Pause the countdown, preserving the remaining time."""
        logger.debug("timer stop")
        self._remaining = self.get_remaining()
        self.is_running = False

    # ── queries ───────────────────────────────────────────────────────

    def get_remaining(self) -> float:
        """Seconds remaining (keeps ticking while running)."""
        if not self.is_running:
            return self._remaining
        return self._timestamp + self._remaining - time.time()

    def get_elapsed(self) -> float:
        """Seconds elapsed since the timer was (re)set."""
        return self._period - self.get_remaining()

    def is_time_up(self) -> bool:
        """Return ``True`` when the countdown has expired."""
        return self.get_remaining() < 0

    # ── formatting ────────────────────────────────────────────────────

    @staticmethod
    def format(remaining: float) -> str:
        """Format *remaining* seconds as ``MM:SS``."""
        minutes = int(remaining / 60)
        seconds = int(remaining) - minutes * 60
        return f"{minutes:02d}:{seconds:02d}"

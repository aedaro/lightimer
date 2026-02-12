"""Placeholder tests for the Lightimer UI.

Full UI testing requires a display (or Xvfb on CI).
"""

import unittest


class TestLightimerApp(unittest.TestCase):
    """Smoke-test placeholder — expand with headless tests as needed."""

    def test_import(self) -> None:
        """The package should be importable without a running display."""
        from lightimer.config import INIT_DURATION_S  # noqa: F401
        from lightimer.timer import StaticTimer  # noqa: F401


if __name__ == "__main__":
    unittest.main()

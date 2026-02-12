"""Unit tests for lightimer.timer.StaticTimer."""

import time
import unittest

from lightimer.timer import StaticTimer

DURATION_S = 2


class TestStaticTimer(unittest.TestCase):
    def setUp(self) -> None:
        self.cut = StaticTimer(DURATION_S)

    def tearDown(self) -> None:
        del self.cut

    # ── construction / set ────────────────────────────────────────────

    def test_ctor_remaining_equals_period(self) -> None:
        self.assertEqual(self.cut.get_remaining(), DURATION_S)

    def test_set_updates_remaining(self) -> None:
        self.cut.set(20)
        self.assertEqual(self.cut.get_remaining(), 20)

    # ── start / stop ──────────────────────────────────────────────────

    def test_start_sets_running(self) -> None:
        self.cut.start()
        self.assertTrue(self.cut.is_running)
        t0 = time.time()
        time.sleep(1)
        t1 = time.time()
        self.assertAlmostEqual(self.cut.get_elapsed(), t1 - t0, places=1)

    def test_stop_freezes_time(self) -> None:
        self.cut.start()
        time.sleep(1)
        self.cut.stop()
        self.assertFalse(self.cut.is_running)
        remaining = self.cut.get_remaining()
        elapsed = self.cut.get_elapsed()
        time.sleep(1)
        self.assertEqual(self.cut.get_remaining(), remaining)
        self.assertEqual(self.cut.get_elapsed(), elapsed)

    # ── remaining / elapsed ───────────────────────────────────────────

    def test_remaining_plus_elapsed_equals_period(self) -> None:
        self.cut.start()
        time.sleep(1)
        self.cut.stop()
        self.assertEqual(
            self.cut.get_remaining(), DURATION_S - self.cut.get_elapsed()
        )

    def test_elapsed_plus_remaining_equals_period(self) -> None:
        self.cut.start()
        time.sleep(1)
        self.cut.stop()
        self.assertEqual(
            self.cut.get_elapsed(), DURATION_S - self.cut.get_remaining()
        )

    # ── time-up ───────────────────────────────────────────────────────

    def test_is_time_up(self) -> None:
        self.cut.start()
        self.assertFalse(self.cut.is_time_up())
        time.sleep(DURATION_S)
        self.assertTrue(self.cut.is_time_up())

    # ── formatting ────────────────────────────────────────────────────

    def test_format(self) -> None:
        self.assertEqual(StaticTimer.format(1), "00:01")
        self.assertEqual(StaticTimer.format(59), "00:59")
        self.assertEqual(StaticTimer.format(60), "01:00")
        self.assertEqual(StaticTimer.format(5999), "99:59")


if __name__ == "__main__":
    unittest.main()

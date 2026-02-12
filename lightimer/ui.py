"""Tkinter-based countdown timer UI."""

from __future__ import annotations

import logging
import os
import sys
import tkinter as tk

from lightimer.config import (
    BG_COLOR,
    HEIGHT_H,
    HEIGHT_V,
    ICON_PATH,
    INIT_DURATION_S,
    LEVEL_COLOR,
    LIN_GAP,
    Orientation,
    REFRESH_CYCLE_MS,
    RGB_MAX,
    TIME_COLOR,
    TIME_FONT,
    WIDTH_H,
    WIDTH_V,
    WIN_GAP,
)
from lightimer.sound import play_notification
from lightimer.timer import StaticTimer

logger = logging.getLogger(__name__)

# ── Orientation look-up tables ────────────────────────────────────────
_DIMENSIONS: dict[Orientation, tuple[int, int]] = {
    Orientation.VERTICAL: (WIDTH_V, HEIGHT_V),
    Orientation.HORIZONTAL: (WIDTH_H, HEIGHT_H),
}

_LEVEL_AXIS: dict[Orientation, int] = {
    Orientation.VERTICAL: HEIGHT_V,
    Orientation.HORIZONTAL: WIDTH_H,
}

_TEXT_GAP: dict[str, int] = {
    "linux": LIN_GAP,
    "win32": WIN_GAP,
}

# Number of digits in the MM:SS entry (0‥3)
_NUM_DIGITS = 4


class LightimerApp(tk.Frame):
    """Main application frame for the Lightimer countdown UI."""

    # ── construction ──────────────────────────────────────────────────

    def __init__(self, master: tk.Tk, *, lean: bool = False) -> None:
        super().__init__(master)
        self.master: tk.Tk = master
        self.lean = lean

        self._configure_window()

        self.duration: float = INIT_DURATION_S
        self._pre_dur: float = self.duration
        self.timer = StaticTimer(self.duration)

        self.orientation = Orientation.VERTICAL

        # Window positions per orientation (width, height, x, y)
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        self._win_pos: dict[Orientation, list[int]] = {
            Orientation.VERTICAL: [
                WIDTH_V,
                HEIGHT_V,
                sw - (WIDTH_V + 25),
                sh // 2 - HEIGHT_V // 2,
            ],
            Orientation.HORIZONTAL: [
                WIDTH_H,
                HEIGHT_H,
                sw - 3 * WIDTH_H // 2,
                sh - (HEIGHT_H + 40),
            ],
        }
        self._apply_geometry()
        self.pack()

        # Digit-entry state
        self._cstate: int = 0
        self._cdigits: list[str | int] = ["-", "-", "-", "-"]

        self._build_canvas()
        self._bind_events()
        self.redraw_canvas()

    # ── window helpers ────────────────────────────────────────────────

    def _configure_window(self) -> None:
        self.master.title("Lightimer")
        icon = tk.PhotoImage(file=_resource_path(ICON_PATH))
        self._icon_ref = icon  # prevent GC
        self.master.call("wm", "iconphoto", self.master._w, icon)
        self.master.attributes("-topmost", True)

        if self.lean:
            if sys.platform == "linux":
                self.master.attributes("-type", "splash")
            elif sys.platform == "win32":
                self.master.overrideredirect(True)
        else:
            if sys.platform == "linux":
                self.master.attributes("-type", "dialog")

    def _apply_geometry(self) -> None:
        d = self._win_pos[self.orientation]
        self.master.geometry(f"{d[0]}x{d[1]}+{d[2]}+{d[3]}")

    # ── canvas setup ──────────────────────────────────────────────────

    def _build_canvas(self) -> None:
        w, h = _DIMENSIONS[self.orientation]
        highlight_opts: dict = (
            dict(
                highlightbackground=TIME_COLOR,
                highlightthickness=1,
                highlightcolor=TIME_COLOR,
                relief=tk.FLAT,
            )
            if self.lean
            else dict(highlightthickness=0)
        )

        self.canvas = tk.Canvas(
            self, width=w, height=h, bd=0, bg=BG_COLOR, **highlight_opts
        )
        self.level = self.canvas.create_rectangle(0, 0, w, h, fill=LEVEL_COLOR, width=0)
        self.lead_line = self.canvas.create_rectangle(
            0, 0, w, 1, fill=LEVEL_COLOR, width=0
        )

        gap = _TEXT_GAP.get(sys.platform, WIN_GAP)
        self.text = self.canvas.create_text(
            w / 2,
            gap,
            text=self.timer.format(self.duration),
            font=TIME_FONT,
            fill=TIME_COLOR,
        )
        self.canvas.pack()

    def _bind_events(self) -> None:
        c = self.canvas
        c.bind("<Button-3>", self._on_click)
        c.bind("<ButtonPress-1>", self._on_motion_start)
        c.bind("<B1-Motion>", self._on_motion)
        c.bind("<ButtonRelease-1>", self._on_motion_stop)
        c.bind("<space>", self._on_click)
        c.bind("<Double-Button-3>", self._on_double_click)
        c.bind("<Return>", self._on_double_click)
        c.bind("<KP_Enter>", self._on_double_click)
        c.bind("t", self._on_toggle)
        if sys.platform == "win32":
            c.bind("l", self._on_lean)
        c.bind("<Key>", self._on_change_time)
        c.bind("<Escape>", self._on_close)
        c.bind("<F1>", self._on_help)
        c.focus_set()

    # ── canvas orientation ────────────────────────────────────────────

    def _config_canvas_for(self, orient: Orientation) -> None:
        w, h = _DIMENSIONS[orient]
        self.canvas.config(width=w, height=h)

    def _redraw_level(self, level: float, color: str) -> None:
        """Redraw the level bar with sub-pixel fade for smooth motion.

        A 1 px leading-edge line is drawn at the boundary between the
        black background and the coloured rectangle.  Its colour is
        interpolated between *color* and black according to the
        fractional pixel position, so the bar appears to glide smoothly
        rather than jumping whole pixels.
        """
        w, h = _DIMENSIONS[self.orientation]
        pixel_pos = int(level)
        frac = level - pixel_pos

        if self.orientation is Orientation.VERTICAL:
            self.canvas.coords(self.level, 0, pixel_pos + 1, w, h)
            self.canvas.coords(self.lead_line, 0, pixel_pos, w, pixel_pos + 1)
        else:
            self.canvas.coords(self.level, pixel_pos + 1, 0, w, h)
            self.canvas.coords(self.lead_line, pixel_pos, 0, pixel_pos + 1, h)

        # Fade the leading-edge line: full colour at frac=0 → black at frac≈1
        fade = 1.0 - frac
        r = int(int(color[1:3], 16) * fade)
        g = int(int(color[3:5], 16) * fade)
        b = int(int(color[5:7], 16) * fade)

        self.canvas.itemconfig(self.level, fill=color)
        self.canvas.itemconfig(self.lead_line, fill=f"#{r:02x}{g:02x}{b:02x}")

    # ── event handlers ────────────────────────────────────────────────

    def _on_lean(self, event: tk.Event) -> None:
        self.lean = not self.lean
        pos = self._win_pos[self.orientation]
        if self.lean:
            self.canvas.config(
                highlightbackground=TIME_COLOR,
                highlightthickness=1,
                highlightcolor=TIME_COLOR,
                relief=tk.FLAT,
            )
            _winpos_offset_add(pos, self.master)
            self._apply_geometry()
            self.master.overrideredirect(True)
        else:
            self.master.overrideredirect(False)
            self.canvas.config(highlightthickness=0)
            _winpos_offset_sub(pos, self.master)
            self._apply_geometry()

    def _on_motion_start(self, event: tk.Event) -> None:
        self._offset_x = event.x
        self._offset_y = event.y

    def _on_motion(self, event: tk.Event) -> None:
        w, h = _DIMENSIONS[self.orientation]
        x = self.master.winfo_pointerx() - self._offset_x
        y = self.master.winfo_pointery() - self._offset_y
        self.master.geometry(f"{w}x{h}+{x}+{y}")

    def _on_motion_stop(self, event: tk.Event) -> None:
        w, h = _DIMENSIONS[self.orientation]
        pos = self._win_pos[self.orientation]
        pos[:] = [
            w,
            h,
            self.master.winfo_pointerx() - self._offset_x,
            self.master.winfo_pointery() - self._offset_y,
        ]

    def _on_help(self, event: tk.Event) -> None:
        logger.info("Help requested (F1)")

    def _on_close(self, event: tk.Event) -> None:
        self.master.destroy()

    def _on_toggle(self, event: tk.Event) -> None:
        self.orientation = (
            Orientation.HORIZONTAL
            if self.orientation is Orientation.VERTICAL
            else Orientation.VERTICAL
        )
        self._apply_geometry()
        self._config_canvas_for(self.orientation)
        self.redraw_canvas()
        if self._cstate != 0:
            self.canvas.itemconfig(self.text, text="%s%s:%s%s" % tuple(self._cdigits))

    def _on_click(self, event: tk.Event) -> None:
        if self.timer.is_time_up():
            return
        if self.timer.is_running:
            self.timer.stop()
        else:
            self._creset()
            self.timer.start()
            self._on_time_running()

    def _on_double_click(self, event: tk.Event) -> None:
        if self.duration == 0:
            return
        self.timer.stop()
        self.timer.reset()
        self._creset()
        self.redraw_canvas()

    def _on_time_running(self) -> None:
        if not self.timer.is_running:
            return
        self.master.after(REFRESH_CYCLE_MS, self._on_time_running)
        self.redraw_canvas()
        if self.timer.is_time_up():
            self.timer.stop()
            self._notify_timesup()

    def _on_change_time(self, event: tk.Event) -> None:
        if not event.char or not event.char.isdigit():
            self._on_help(event)
            return
        if self.timer.is_running:
            self.timer.stop()
        self._apply_digit(self._cstate, event.char)
        self.canvas.itemconfig(self.text, text="%s%s:%s%s" % tuple(self._cdigits))
        self.timer.set(self.duration)

    # ── drawing ───────────────────────────────────────────────────────

    def redraw_canvas(self) -> None:
        """Update the level bar, colour, and remaining-time label."""
        if self.duration == 0 or self.timer.is_time_up():
            self.canvas.itemconfig(self.level, fill="black")
            self.canvas.itemconfig(self.lead_line, fill="black")
            self.canvas.update_idletasks()
            return

        half = self.duration / 2
        elapsed = self.timer.get_elapsed()
        remaining = self.timer.get_remaining()

        red = int(round(min(RGB_MAX, (elapsed / half) * RGB_MAX)))
        green = max(0, int(round(min(RGB_MAX, (remaining / half) * RGB_MAX))))

        level_size = _LEVEL_AXIS[self.orientation]
        level = (elapsed * level_size) / self.duration
        color = f"#{red:02x}{green:02x}00"
        self._redraw_level(level, color)

        self.canvas.itemconfig(
            self.text,
            text=self.timer.format(remaining),
            fill=TIME_COLOR,
        )
        self.canvas.update_idletasks()

    # ── digit entry ───────────────────────────────────────────────────

    def _creset(self) -> None:
        self._cstate = 0
        self._cdigits = ["-", "-", "-", "-"]

    def _apply_digit(self, position: int, char: str) -> None:
        """Set the digit at *position* (0‥3) and advance the entry state.

        Digit positions correspond to ``M0 M1 : S0 S1``.
        """
        digit = int(char)

        # Position-specific multipliers: [10min, 1min, 10sec, 1sec]
        multipliers = [600, 60, 10, 1]

        if position == 0:
            # Starting a new entry — reset first
            self.timer.reset()
            self._creset()
            self.redraw_canvas()

        if position == 2 and digit > 5:
            # Tens-of-seconds must be 0‥5
            return

        self._cdigits[position] = digit

        if position == 0:
            self._pre_dur = digit * multipliers[position]
        else:
            self._pre_dur += digit * multipliers[position]

        if self._pre_dur != 0:
            self.duration = self._pre_dur

        self._cstate = (position + 1) % _NUM_DIGITS

    # ── notifications ─────────────────────────────────────────────────

    def _notify_timesup(self) -> None:
        play_notification()
        self.canvas.itemconfig(self.text, fill="red")


# ── module-level helpers ──────────────────────────────────────────────


def _resource_path(relative_path: str) -> str:
    """Resolve *relative_path* inside a PyInstaller bundle or the project root."""
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def _winpos_offset_add(pos: list[int], master: tk.Tk) -> None:
    pos[2] += master.winfo_rootx() - master.winfo_x()
    pos[3] += master.winfo_rooty() - master.winfo_y()


def _winpos_offset_sub(pos: list[int], master: tk.Tk) -> None:
    pos[2] -= master.winfo_rootx() - master.winfo_x()
    pos[3] -= master.winfo_rooty() - master.winfo_y()

"""Entry point for the Lightimer application."""

import argparse
import sys
import tkinter as tk

from lightimer.ui import LightimerApp


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lightimer countdown timer")
    parser.add_argument(
        "-l",
        "--lean",
        action="store_true",
        help="start in lean mode",
    )
    parser.add_argument(
        "-s",
        "--sound-file",
        dest="sound_file",
        help="path to a WAV or MP3 file used for the times-up notification",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args(sys.argv[1:])
    root = tk.Tk()
    app = LightimerApp(master=root, lean=args.lean, sound_file=args.sound_file)
    app.mainloop()


if __name__ == "__main__":
    main()

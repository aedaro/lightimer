"""Entry point for the Lightimer application."""

import sys
import tkinter as tk

from lightimer.ui import LightimerApp


def main() -> None:
    is_lean = len(sys.argv) > 1 and sys.argv[1] in ("-l", "--lean")
    root = tk.Tk()
    app = LightimerApp(master=root, lean=is_lean)
    app.mainloop()


if __name__ == "__main__":
    main()

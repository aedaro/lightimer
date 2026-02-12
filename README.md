## Lightimer
A handy countdown timer for mastering time management in [LightingTalks](https://en.wikipedia.org/wiki/Lightning_talk) or other short presentations. It works for Linux and Windows.

### Set up environment
First, clone the *lightimer* repo into your favorite directory.

Next, install [uv](https://docs.astral.sh/uv/getting-started/installation/) — a fast Python package manager:
```
# Linux / macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then install the project and its dependencies:
```
cd <path/to/lightimer>
uv sync
```

Now you're good to go. Run the lightimer:
```
uv run python main.py
```

If a green narrow window can be seen on the right side of your screen... Congratulations! You successfully run the lightimer.

To build a single file binary out of the source code do the following:
```
uv run pyinstaller lightimer.spec
```

or you can specify all parameters for the *pyinstaller* manually:
```
uv run pyinstaller --onefile --icon lightimer.ico --add-data "sound/timesup.wav:sound/" --name lightimer main.py
```

and find the newly installed binary file `lightimer` within the `dist/` folder.

[//]: # (Install on Windows:
pyinstaller --onefile --noconsole --icon lightimer.ico --name lightimer main.py --add-data "sound/timesup.wav;sound/")

### HowTo use the Lightimer
Using the lightimer is pretty simple and straight forward. Run it from command line with `./lightimer` (`lightimer.exe` on Windows). You can start it in lean mode with the argument `-l` (lowercase "L") or `--lean`. (This feature works well in Windows and is rather experimental in Linux.)
Once the lightimer is up and running, you can right-click (`Spacebar`) to start or stop the timer. Double-right-click (`Enter`) resets the timer and it can be started anew.

To toggle between vertical and horizontal type `t`. Hit `l` (lowercase "L") to change into seamless (light) mode. To move window, go left-click and drag. To quit, hit `Esc`.

For changing the duration time, just start typing numbers. Duration time (digital clock) will then be changed from left to right, digit by digit in the format `mm:ss`. During change, the timer can be started at any time. Not typed numbers will automatically be filled with zeroes. E.g. `1-:--` will result in `10:00` or `00:3-` will result in `00:30` accordingly. 

While time is running, the level bar decreases relatively with the elapsed time and changes colour from green to red, to give a visual impression on the remaining time. Once time is up, the level bar decreased completely and a notification sound is played. Digits on the clock turn red. The timer can be reset and used again.

Have fun!
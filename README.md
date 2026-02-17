## Lightimer
A handy countdown timer for mastering time management in [Lightning talks](https://en.wikipedia.org/wiki/Lightning_talk) or other short presentations. It works for Linux, Windows and probably on Mac (not tested yet).

![Lightimer](pix/lightimer.png)

### Set up environment
First, install [python3-tk](https://docs.python.org/3/library/tkinter.html) and [uv](https://docs.astral.sh/uv/getting-started/installation/).
Then, clone the __lightimer__ repo into your favorite directory and off you go:

Install the project and its dependencies:
```
cd <path/to/lightimer>
uv sync
```

Now you're good to go. Run the Lightimer:
```
uv run python main.py
```

If a green narrow window can be seen on the right side of your screen... Congratulations! You successfully run the Lightimer.

To build a single file binary out of the source code, do the following:
```
uv run pyinstaller lightimer.spec
```

or you can specify all parameters for the _pyinstaller_ manually:
```
uv run pyinstaller --onefile --icon lightimer.ico --add-data "sound/timesup.wav:sound/" --name lightimer main.py
```

and find the newly installed binary file `lightimer` (`lightimer.exe` on Windows) within the `dist/` folder.

[//]: # (Install on Windows:
pyinstaller --onefile --noconsole --icon lightimer.ico --name lightimer main.py --add-data "sound/timesup.wav;sound/")

### How to use the Lightimer
Using the Lightimer is pretty simple and straight forward. Run it from command line with `./lightimer(.exe)`. You can start it in lean mode with the argument `-l` (lowercase "L") or `--lean`. You can also provide a custom notification sound via `-s <path/to/file.wav|mp3>` or `--sound-file <path/to/file.wav|mp3>`. If no sound file is provided, Lightimer uses the default bundled sound file. Once the Lightimer is up and running, you can right-click (`Spacebar`) to start or stop the timer. Double-right-click (`Enter`) resets the timer and it can be started anew.

To toggle between vertical and horizontal type `t`. Hit `l` (lowercase "L") to change into seamless (light) mode (works only in Windows). To move window, go left-click and drag. To quit, hit `Esc`.

For changing the duration time, just start typing numbers. Duration time (digital clock) will then be changed from left to right, digit by digit in the format `mm:ss`. During change, the timer can be started at any time. Not typed numbers will automatically be filled with zeroes. E.g. `1-:--` will result in `10:00` or `00:3-` will result in `00:30` accordingly. 

While time is running, the level bar decreases relatively with the elapsed time and changes color from green to red, to give a visual impression on the remaining time. Once time is up, the level bar decreased completely and a notification sound is played. Digits on the clock turn red. The timer can be reset and used again.

Have fun!

### License

This project is licensed under MIT License - see the [LICENSE](LICENSE) file.

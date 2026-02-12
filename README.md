## Lightimer
A handy countdown timer for mastering time management in [LightingTalks](https://inside-docupedia.bosch.com/confluence/display/BEGSC/Lightning+Talks) or other short presentations. It works for Linux and Windows.

### Set up environment
First, clone the *lightimer* repo into your favorite directory.

Next, in order to make it work, we need to setup the environment. All necessary modules are defined in the environment.yml file. First install *Miniconda* (Anaconda) from the [website](https://docs.conda.io/en/latest/miniconda.html) for your system (e.g. Linux):
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

Reopen your bash and install the environment
```
cd <path/to/lightimer>
conda env create -f environment.yml
```

and activate it
```
conda activate lightimer
```

Now, if everything is set up you should see the environment name *(lightimer)* before your regular prompt. Finally, you're good to go. Go ahead and run your lightimer:
```
python main.py
```

If a green narrow window can be seen on the right side of your screen... Congratulations! You successfully run the lightimer.

To build a single file binary out of the source code do the following:
```
pyinstaller lightimer.spec
```

or you can specify all parameters for the *pyinstaller* manually:
```
pyinstaller --onefile --icon lightimer.ico --add-data "sound/timesup.wav:sound/" --name lightimer main.py
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
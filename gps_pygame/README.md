# bladeGPS-Game
> See [bladeGPS](../Readme.md) for readme of the original program.

Written in Ubuntu 18.04.2 LTS using Python 3.6.8, works with bladeRF.

An extended version of **bladeGPS** where, instead of changing the position using the keyboard, it listenes to a `.txt`-file when in `interactive` mode. You may start bladeGPS in any static position using e.g. `/bladegps -e brdc1720.19n -i -l 30,-20,100`. This Python program will then, when run, write the file that bladeGPS reads from.

The program uses the Python packages
- `subprocess`
- `multiprocessing`
- `pygame`
- `geographiclib`
- `serial`
- `PIL`
- `osmviz`
- `numpy`

You run the program with
~~~
python3 main.py
~~~
and get a promt weather to use real time GNSS-coordinates or a static position. For real time coordinates you will need a GNSS receiver. The program is tested to work with u-blox EVK-M8C.

A `.kml` file is written which can be opened using Google Earh Pro, so for better visualization, Google Earth Pro is recommended. When run, the program will also write the coordinates to the file `log.txt` to be able to look back at the recorded data.

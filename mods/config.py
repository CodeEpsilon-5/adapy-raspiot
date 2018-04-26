import RPi.GPIO as gpio
from typing import Dict, Callable

io = gpio
io.setmode(io.BCM)


loaded_mods = {} # type: Dict[str, Dict[str, Callable]]

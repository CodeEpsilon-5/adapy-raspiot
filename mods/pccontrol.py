import json
import re
from . import config
from typing import Any
from wakeonlan import send_magic_packet


def wakeup(val: Any):
    with open('./prefs.json', 'r') as f:
        settings = json.loads(''.join(f.readlines()))
    addr = settings['pccontrol']['mac']
    send_magic_packet(addr)


def echo(val: Any):
    print("echo")


def switchrelay(st: bool):
    io = config.io
    with open('./prefs.json', 'r') as f:
        settings = json.loads(''.join(f.readlines()))
    pin = settings['pccontrol']['rlpin']
    io.setup(pin, io.OUT)
    print(f'Pin {pin}set to mode OUTPUT')

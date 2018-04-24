import mods.config as config
import datetime
import importlib
import json
import logging
import os
import sy
from Adafruit_IO import MQTTClient
from mods import essentials
from schema import (
        And,
        Optional,
        Or,
        Schema,
        SchemaError,
        Use,
)
from systemd.journal import JournalHandler
from typing import Callable, Dict, Tuple, List

# Load json settings
with open('prefs.json', 'r') as f:
    settings = json.loads(''.join(f.readlines()))

# Setup logging
log = logging.getLogger('AdaPy-RasPIot')
fh = logging.FileHandler('{}-client.log'.format(datetime.datetime.now()
                         .strftime('%y%m%d_%H%M%S')))
fh_fm = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - \
                            %(message)s\r')
jh = JournalHandler()

jh_fm = logging.Formatter('%(levelname)s - %(message)s')

fh.setLevel(logging.DEBUG)
jh.setLevel(logging.INFO)

fh.setFormatter(fh_fm)
jh.setFormatter(jh_fm)

log.addHandler(fh)
log.addHandler(jh)


# MQTT client callbacks
def connected(client):
    log.info('Conectado ao servidor Adafruit.IO com sucesso.')
    client.subscribe('HomeAuto')


def disconnected(client):
    log.info('Desconectado')
    sys.exit(0)


def message(client, feed_id, payload):
    try:
        data = json.loads(payload)
    except json.decoder.JSONDecodeError as e:
        log.error('Invalid JSON payload')
        return
    log.debug(f'Incoming Payload: {data}')
    try:
        grp = data['group']
        cmd = data['command']
        loaded_mods[grp][cmd](data['value'])
        assert loaded_mods.get(data['group']) is not None
        log.info(f'Command Executed: {grp}.{cmd}')
    except KeyError:
        log.error('Group or Command not found')
        log.debug(f'group: {data["group"]} command: {data["command"]}')
        log.debug(f'mods + commands: {loaded_mods}')


def main():
    while True:
        pass


client = MQTTClient(
        settings['adafruit']['username'],
        settings['adafruit']['key'],
        )

client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message

loaded_mods: Dict[str, Dict[str, Callable]] = config.loaded_mods

if __name__ == '__main__':
    loaded_mods['essentials'] = {}
    funcs = list(filter(lambda x: not x.startswith('__'), dir(essentials)))
    for func in funcs:
        loaded_mods['essentials'][func] = getattr(essentials, func)

    client.connect()
    client.loop_background()
    main()

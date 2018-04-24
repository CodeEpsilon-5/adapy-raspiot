import datetime
import importlib
import json
import logging
import os
import sy
from Adafruit_IO import MQTTClient
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

if __name__ == '__main__':
    client.connect()
    client.loop_background()
    main()

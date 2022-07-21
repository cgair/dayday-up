#!/usr/bin/env python

import time
import logging
from binance.lib.utils import config_logging
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

# config_logging(logging, logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


def message_handler(message):
    logging.info(message)


my_client = UMFuturesWebsocketClient()
my_client.start()

my_client.kline(
    symbol="btcusdt",
    id=12,
    interval="1h",
    callback=message_handler,
)

time.sleep(10)

logging.debug("closing ws connection")
my_client.stop()

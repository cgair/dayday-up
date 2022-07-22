"""
@author chenge
"""
# Specify the currency and specify the alarm price to trigger (multiple currencies and prices can be set at the same time) 
# The example of the message body is as follows:
# "ETHUSDT Crossing 1111.74"
import logging
import websocket
from dingding_client import send_msg, send_msg_at
from start import CROSSING_FMT, VOLUME_FMT

KLINE = 'wss://fstream.binance.com/ws/{}@kline_1m' # TODO interval should be configurable


class UMWebsocketClient(object):
    def __init__(self, url, critical_price, volume=None):
        self.ws = None
        self.url = url
        self.critical_price = critical_price
        self.volume = volume

    def on_message(self, obj, message):
        logging.debug(f"received: {message}")
        self._is_crossing(message)
        if self.volume:
            self._is_surpassing(message)

    def on_close(self, close_status_code, close_msg):
        logging.debug(f'closed: {close_status_code}, {close_msg}')
    
    def start(self):
        # if kind == 'kline':
        # Enable running status tracking. 
        # It is best to open it when debugging, so as to track and locate the problem.
        # websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_close=self.on_close)

        self.ws.run_forever()

    def _is_crossing(self, message):
        symbol = message['s']
        tx_num = message['v'] # Transaction numbers during this K line
        if tx_num >= self.volume:
            content = VOLUME_FMT.format(symbol, 1, self.volume, tx_num)
            send_msg_at(content)

    def _is_surpassing(self, message):
        symbol = message['s']
        tx_price_h = message['h']    # The highest transaction price during this K line
        tx_price_l = message['l']    # The lowest transaction price during this K line
        if tx_price_h > self.critical_price and tx_price_l < self.critical_price:
            content = CROSSING_FMT.format(symbol, self.critical_price)
            send_msg(content)


# def start_websocket(**kwargs):
def start_websocket(symbol, critical_price, volume=None):
    kline_url = KLINE.format(symbol.lower())
    umc = UMWebsocketClient(kline_url, critical_price, volume)
    umc.start()



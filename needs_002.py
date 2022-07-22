"""
@author chenge
"""
# Specify the currency and specify the alarm price to trigger (multiple currencies and prices can be set at the same time) 
# The example of the message body is as follows:
# "ETHUSDT Crossing 1111.74"
import logging
import demjson
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
        message = demjson.decode(message)
        logging.debug(f"received: {message}")
        self._is_crossing(message)
        if self.volume:
            self._is_surpassing(message)

    def on_close(self, close_status_code, close_msg):
        logging.debug(f'closed: {close_status_code}, {close_msg}')
    
    def on_error(self, error):
        global reconnect_count
        if type(error)==ConnectionRefusedError or type(error)==websocket._exceptions.WebSocketConnectionClosedException:
            logging.info(f"Attempting to reconnect {reconnect_count}")
            reconnect_count += 1
            if reconnect_count < 100:
                self.start()
        else:
            logging.error("encounter other error!")
    
    def start(self):
        # if kind == 'kline':
        # Enable running status tracking. 
        # It is best to open it when debugging, so as to track and locate the problem.
        # websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_close=self.on_close)
        try:
            self.ws.run_forever()
        except KeyboardInterrupt:
            self.ws.close()  
        except:
            self.ws.close() 

    def _is_crossing(self, message):
        symbol = message['s']
        tx_num = message['k']['v'] # Transaction numbers during this K line
        if float(tx_num) >= float(self.volume):
            content = VOLUME_FMT.format(symbol, 1, self.volume, tx_num)
            send_msg_at(content)

    def _is_surpassing(self, message):
        symbol = message['s']
        tx_price_h = message['k']['h']    # The highest transaction price during this K line
        tx_price_l = message['k']['l']    # The lowest transaction price during this K line
        if float(tx_price_h) > float(self.critical_price) and float(tx_price_l) < float(self.critical_price):
            content = CROSSING_FMT.format(symbol, self.critical_price)
            send_msg(content)


# def start_websocket(**kwargs):
def start_websocket(symbol, critical_price, volume=None):
    kline_url = KLINE.format(symbol.lower())
    umc = UMWebsocketClient(kline_url, critical_price, volume)
    umc.start()



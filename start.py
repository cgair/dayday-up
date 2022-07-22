#!/usr/bin/env python
import logging
import threading

from binance.lib.utils import config_logging
from apscheduler.schedulers.blocking import BlockingScheduler

from needs_001 import *
from needs_002 import *
from dingding_client import send_msg
from utils import *
from config import Config

# SYMBOLS=["BTCUSDT", "ETHUSDT", "DOGEUSDT"]
QUOTATION_FMT="-------------------------\n[{}]\n{}: ${} U\n时间: {}\n过去1天的涨跌幅: {:.2%}\n"
CROSSING_FMT="{} 穿过(Crossing) {}."
VOLUME_FMT="{} {}分钟成交量超过{} 当前成交量为: {}."


# Get symnols latest prices
def job_1(config: Config):
    to_send = ""
    symbols = config.config['need1']['symbols']
    for s in symbols:
        response = timed_quotation_price(s)
        limit_usage = int(response['limit_usage']['x-mbx-used-weight-1m'])
        access_limit(limit_usage)

        # FIXME data is None
        price = response['data']["price"]
        # 13 位
        time = response['data']["time"]
        fmt_time = to_beijingtime(time)
        up_down = timed_quotation_up_down(s)
        content = QUOTATION_FMT.format(s, s, price, fmt_time, up_down)
        to_send = to_send + content
    response = send_msg(to_send)
    logging.info(response)
    # logging.info(to_send)
            

def job_2(config: Config):
    config = config['need2']
    handler = []
    for value in config.values():
        volume = None
        symbol, critical_price = value['symbols'], value['critical_price']
        if 'volume' in value.keys():
            volume = value['volume'] 
        # params = {'symbol': symbol, 'critical_price': critical_price}
        t = threading.Thread(target=start_websocket, args=(symbol, critical_price, volume))
        t.start()
        handler.append(t)
    for h in handler:
        h.join()


def main():
    config = Config()
    # BlockingScheduler
    sched = BlockingScheduler()
    sched.add_job(job_1, 'interval', args=[config], hours=4, id='need-001', start_date='2022-07-21 08:00:00', end_date='2022-07-28 13:00:00')
    # sched.add_job(job_1, 'interval', args=[config], minutes=1, id='need-001')
    sched.start()
    job_2()


if __name__ == '__main__':
    config_logging(logging, logging.DEBUG)
    # config_logging(logging, logging.INFO)
    main()

    # the following code is only for test
    # 
    # job_1()
    
    # import os
    # print(os.path.dirname(__file__))
    # config = Config()
    # print(config.__dict__)
    # import toml
    # conf = toml.load("config/config.toml")['need2']
    # # for key in conf.keys():
    # #     print(f"{key}: {conf[key]}")
    # for value in conf.values():
    #     symbol, critical_price = value['symbols'], value['critical_price']
    #     print(f"symbol: {symbol}, critical_price: {critical_price}")
    #     if 'volume' in value.keys():
    #         volume = value['volume'] 
    #         print(f"volume: {volume}")
    # conf = toml.load("config/config.toml")
    # job_2(conf)



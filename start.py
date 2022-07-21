#!/usr/bin/env python
import logging

from binance.lib.utils import config_logging
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from needs_001 import *
from dingding_client import send_msg
from utils import *

SYMBOLS=["BTCUSDT", "ETHUSDT"]
# SYMBOLS=["ETHUSDT"]   # for test
QUOTATION_FMT="-------------------------\n[{}]\n{}: ${} U\n时间: {}\n过去1天的涨跌幅: {:.2%}\n"


# Get symnols latest prices
def job_1():
    to_send = ""
    for s in SYMBOLS:
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
            

def main():
    # BlockingScheduler
    sched = BlockingScheduler()
    sched.add_job(job_1, 'interval', hours=4, id='need-001', start_date='2022-07-21 08:00:00', end_date='2022-07-28 13:00:00')
    sched.start()


if __name__ == '__main__':
    config_logging(logging, logging.DEBUG)
    # config_logging(logging, logging.INFO)
    # main()

    # for test
    job_1()
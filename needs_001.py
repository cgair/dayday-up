#!/usr/bin/env python
import logging

from typing import List
from binance.um_futures import UMFutures

from utils import access_limit

PARAMS={
    'show_limit_usage': True,
    'key': "dlWhYRUhMmDaWujW5Pp22uvpW6stXaeODyHXOnvf3DluxuywTVmIotnX2nisoOtP"
    # 'show_header': True
}


def timed_quotation_price(symbol: str):
    um_futures_client = UMFutures(**PARAMS)
    response = um_futures_client.ticker_price(symbol)
    return response


# FIXME data is None
def timed_quotation_up_down(symbol: str):
    um_futures_client = UMFutures(**PARAMS)
    response = um_futures_client.ticker_24hr_price_change(symbol)
    limit_usage = int(response['limit_usage']['x-mbx-used-weight-1m'])
    access_limit(limit_usage)
    first_id = response['data']["firstId"]
    last_id = response['data']["lastId"]
    logging.debug(f"Within 24 hours, the id of the first transaction is {first_id}, and the id of the last transaction is {last_id}")
    
    param = { "limit": 1, "fromId": int(first_id)}
    response = um_futures_client.historical_trades(symbol, **param)
    limit_usage = int(response['limit_usage']['x-mbx-used-weight-1m'])
    access_limit(limit_usage)
    denominator = response['data'][0]["price"]  # I'm not sure if there is a value all the time

    param = { "limit": 1, "fromId": int(last_id)}
    response = um_futures_client.historical_trades(symbol, **param)
    limit_usage = int(response['limit_usage']['x-mbx-used-weight-1m'])
    access_limit(limit_usage)
    molecular = response['data'][0]["price"]
    up_down = (int(float(molecular)) - int(float(denominator)))/ int(float(denominator))

    return up_down
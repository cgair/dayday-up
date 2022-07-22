#!/usr/bin/env python
import pytest
import time

from config import Config

def test_hot_reload():
    config = Config()
    while True:
        # capture stdout/stderr output
        print(config.config)
        time.sleep(5)

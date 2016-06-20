#!/usr/bin/env python2
# coding: utf-8

from __future__ import division

import re
import time
import easytrader
from download import download

PLATFORM = 'ht'
CONFIG_FILE = 'account.json'

NET_RATE = 94053

class trader:
    def __init__(self):
        self.user = easytrader.use(PLATFORM)
        self.user.prepare(CONFIG_FILE)
        self.asset = self.user.balance[0].get('asset_balance')

    def get_message(self):
        date = time.strftime('%Y-%m-%d')
        net_value = self.asset / NET_RATE
        return str(net_value)


if __name__ == '__main__':
    t = trader()
    print t.get_message()

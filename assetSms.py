#!/usr/bin/env python2
# coding: utf-8

import re
import time

from trader import trader
from sms import smsSender

def assetSms():
    asset = trader().get_message()
    sms = smsSender()
    recievers = ['13686898576']
    message = u'%s\n 今日净值: %s 【From StockFucker】 ' % (time.strftime('%Y%m%d'), asset)
    for reciever in recievers:
        sms.sender(reciever, message)

if __name__ == '__main__':
    assetSms()

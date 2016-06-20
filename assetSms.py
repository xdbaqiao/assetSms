#!/usr/bin/env python2
# coding: utf-8

import re
import time
import json
from trader import trader
from sms import smsSender

SMS_CONFIG = 'SMS.json'

def analysis_json(file_name):
    with open(file_name) as f:
        djson = json.load(f)
        return djson.get('user'), djson.get('passwd'), djson.get('recievers')

def assetSms():
    user, passwd, a_reciever = analysis_json(SMS_CONFIG)

    asset = trader().get_message()
    sms = smsSender(user, passwd)
    recievers = a_reciever.split(',')

    message = u'%s日净值: %.4f 【From StockFucker】 ' % (time.strftime('%Y-%m-%d'), float(asset))
    for reciever in recievers:
        sms.sender(reciever, message)

if __name__ == '__main__':
    assetSms()

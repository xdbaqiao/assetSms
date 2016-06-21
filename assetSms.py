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
    last_info = ''
    message = ''
    with open('data.csv') as f:
        last_info = f.readlines()[-1]
    user, passwd, a_reciever = analysis_json(SMS_CONFIG)
    asset = trader().get_message()
    [date, last_asset] = last_info.split(',') if ',' in last_info else ['', '']
    if date and last_asset:
        message += u'%s日净值: %.4f, ' % (date, float(last_asset))
        up_rate = (float(asset) - float(last_asset))/float(last_asset) * 100
    message += u'%s日净值: %.4f' % (time.strftime('%Y-%m-%d'), float(asset))
    message += u', 涨 +%.2f%%' % up_rate if up_rate > 0 else u', 跌 -%.2f%%' % up_rate
    message += u'【From StockFucker】 ' 

    sms = smsSender(user, passwd)
    recievers = a_reciever.split(',')
    for reciever in recievers:
        sms.sender(reciever, message)

if __name__ == '__main__':
    assetSms()

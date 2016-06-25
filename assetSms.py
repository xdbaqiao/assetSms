#!/usr/bin/env python2
# coding: utf-8

import re
import time
import json
from trader import trader
from sms import smsSender

SMS_CONFIG = 'SMS.json'

def analysis_json(file_name):
    ''' 返回短信账户用户名、密码，短信接收者和对应的份额
    '''
    with open(file_name) as f:
        djson = json.load(f)
        return djson.get('user'), djson.get('passwd'), djson.get('recievers'), djson.get('portion')

def assetSms(cache=False):
    last_info = ''
    info = ''
    message = ''
    with open('data.csv') as f:
        last_info, info = f.readlines()[-2:]
    user, passwd, a_reciever, a_portion = analysis_json(SMS_CONFIG)
    recievers = a_reciever.split(',')
    portions = a_portion.split(',')

    assert len(recievers) == len(portions)
    if not cache:
        sum_portions = sum([float(i) for i in portions])
        asset = trader().get_message(sum_portions)
        last_info = info
    else:
        asset = info.split(',')[1]

    # 昨日净值
    [date, last_asset] = last_info.split(',') if ',' in last_info else ['', '']

    # 拼接短信内容
    if date and last_asset:
        #message += u'%s日净值: %.4f，' % (date, float(last_asset))
        up_rate = (float(asset) - float(last_asset))/float(last_asset) * 100
    message += u'%s日净值: %.4f' % (time.strftime('%Y-%m-%d'), float(asset))
    message += u'，涨 +%.2f%%' % up_rate if up_rate > 0 else u'，跌 %.2f%%' % up_rate

    sms = smsSender(user, passwd)
    for num, reciever in enumerate(recievers):
        send_message = message + u'，您的账户总资产：%.2f ' % (float(portions[num]) * float(asset))
        send_message += u'【From StockFucker】 ' 
        sms.sender(reciever, send_message)

if __name__ == '__main__':
    assetSms(cache=False)

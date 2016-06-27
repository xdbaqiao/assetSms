#!/usr/bin/env python2
# coding: utf-8

import re
import urllib
from download import download

class smsSender:
    def __init__(self, user, passwd):
        self.user = user
        self.passwd = passwd
        self.refer = 'https://wapmail.10086.cn/index.htm'
        self.D = download(refer=self.refer)
        self.url = 'https://wapmail.10086.cn/index.htm'


    def login(self):
        bag = {}
        bag['ur'] = self.user
        bag['pw'] = self.passwd
        bag['apct'] = 'on'
        bag['apc'] = '1'
        self.D.get(self.refer)
        m_url, html = self.D.post(url=self.url, data=bag)
        if 'sid' in m_url:
            print 'Login success!'
            return m_url
        else:
            print 'Login fail!'
            return False

    def senderSMS(self, reciever, message):
        message = message.encode('utf8')
        url = 'http://f.10086.cn/im5/chat/sendNewGroupShortMsg.action'
        m_url = self.login()
        w3_url = 'http://m.mail.10086.cn/ws12/w3/w3smsend'
        sid = re.compile(r'sid=([^&]+)').search(m_url).groups()[0]
        vn = re.compile(r'vn=([^&]+)').search(m_url).groups()[0]
        data = {'sid':sid , 'vn':vn, 'behaviorData':'105799_1', '':'', 'cmd':'40'}
        m_url, info = self.D.post(w3_url, data)
        if 'userFreeCount' in info:
            info = urllib.unquote(info)
            num = re.compile(r'"userFreeCount":(\d+)').search(info).groups()[0]
            print 'The remaining SMS num: %s' % num
            if num > 0:
                data = {'sid':sid , 'vn':vn, 'cmd':'2', '':'', 'content':message, 'reciever': reciever}
                m_url, info = self.D.post(w3_url, data)
                if info:
                    print 'Send success!'
                else:
                    print 'Send fail'
            else:
                print 'Sender is no money!'

    def senderEmail(self, reciever, message):
        message = message.encode('utf8')
        url = 'http://f.10086.cn/im5/chat/sendNewGroupShortMsg.action'
        m_url = self.login()
        w3_url = 'http://m.mail.10086.cn/wp12/w3/mfoperation'
        sid = re.compile(r'sid=([^&]+)').search(m_url).groups()[0]
        vn = re.compile(r'vn=([^&]+)').search(m_url).groups()[0]
        data = {'sid':sid , 'vn':vn, 'cmd':'1000', '':'', 'action':'261', 'e':'101013'}
        self.D.post(w3_url, data)
        data = {'sid':sid , 'vn':vn, 'cmd':'2', '':'', 'content':message, 
                'reciever': '%s,' % reciever,
                'subject': '今日净值',
                'showOneRcpt': '0',
                'priority': '0',
                'requestReadReceipt': '0',
                'isHtml': '0',
                'timing': 'false'}
        info = self.D.post('http://m.mail.10086.cn/wp12/w3/sendmail', data)
        info = urllib.unquote(info[1])
        if '"eroerCode":0,' in info:
            print 'Send success!'
        else:
            m = re.compile(r'"msg":"([^"]+)').search(info)
            print 'ERROR: %s' % urllib.unquote(m.groups()[0])

if __name__ == '__main__':
    import json
    with open('SMS.json') as f:
        djson = json.load(f)
        user = djson.get('user')
        passwd = djson.get('passwd')
        a_reciever = djson.get('recievers')
    sms = smsSender(user, passwd)
    recievers = a_reciever.split(',')
    message = u'今日净值: 1.115, 收益: +11.5% 【From StockFucker】'
    for reciever in recievers:
        sms.senderSMS(reciever, message)

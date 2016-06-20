#!/usr/bin/env python2
# coding: utf-8

import re
import urllib
from download import download

class smsSender:
    def __init__(self):
        self.refer = 'https://wapmail.10086.cn/index.htm'
        self.D = download(refer=self.refer)
        self.url = 'https://wapmail.10086.cn/index.htm'

    def login(self):
        bag = {}
        bag['ur'] = '13686898576'
        bag['pw'] = 'yexinjing16122'
        bag['apct'] = 'on'
        bag['apc'] = '1'
        self.D.get(self.refer)
        m_url, html = self.D.post(url=self.url, data=bag)
        if '">退出' in html:
            print 'Login success!'
            return m_url
        else:
            print 'Login fail!'
            return False

    def sender(self, reciever, message):
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

if __name__ == '__main__':
    sms = smsSender()
    recievers = ['13686898576']
    message = u'今日净值: 1.115, 收益: +11.5% 【From StockFucker】'
    for reciever in recievers:
        sms.sender(reciever, message)

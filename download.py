#!/usr/bin/python2
# coding:utf8

import urllib
import urllib2
import cookielib

class download:
    '''first_url: the referer in headers
       proxy: the proxy format with ip:port
       is_cookie: whether download with cookie
    '''
    def __init__(self, refer=''):
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0'
        self.headers = {'User-Agent': self.user_agent, 'Accept-encoding':'gzip, deflate', 'Referer': refer, 
                'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.MozillaCookieJar()))

    def get(self, url):
        print 'Downloading %s' % url
        request = urllib2.Request(url)
        response = self.opener.open(request)
        html = response.read()
        return html

    def post(self, url, data):
        if isinstance(data, dict):
            data = urllib.urlencode(data)
        request = urllib2.Request(url, data, self.headers)
        response = self.opener.open(request)
        print 'Downloading %s' % url
        html = response.read()
        m_url = response.geturl()
        return m_url, html

if __name__ == '__main__':
    url = 'http://www.baidu.com'
    print download().get(url)

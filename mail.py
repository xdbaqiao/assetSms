#!/usr/bin/env python2
# coding: utf-8

import smtplib  
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

HOST = 'smtp.163.com'  #设置服务器

def _format_addr(message):
    name, addr = parseaddr(message)
    return formataddr((
        Header(name, 'utf-8').encode(),
        addr.encode('utf-8') if isinstance(addr, unicode) else addr
        ))
  
def sendMail(user, passwd, reciever, message):  
    bag = MIMEText(message, _subtype='html', _charset='utf-8')  
    #bag = MIMEText(message, _subtype='plain', _charset='utf-8')  
    bag['Subject'] = Header(u'今日净值', 'utf-8').encode()
    bag['From'] = _format_addr(u'StockFuckers<%s>' % user)
    bag['To'] = _format_addr(u'StockFuckers<%s>' % reciever)
    print 'Sending mail to: %s' % reciever
    try:
        server = smtplib.SMTP(HOST, 25)  
        server.login(user, passwd)  
        server.sendmail(user, [reciever], bag.as_string())  
        server.quit()  
        print 'Send success!'
    except Exception, e:
        print str(e)
        print 'Send Fail!'

if __name__ == '__main__':  
    message = u'<html><body><h3>2016-07-02 日净值</h3><br><h3> 1.155，跌 -0.90%</h3><br><h3>您的账户总资产：21729.25 </h3><br><p>【From StockFucker】 </p></html></body>'

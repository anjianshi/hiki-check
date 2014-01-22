# -*- coding: utf-8 -*-
from __future__ import print_function
import time
from datetime import datetime
import requests
from requests.exceptions import Timeout
import sys
from sae.mail import send_mail
import urllib, urllib2

# 解决 SAE 中 requests 无法正常访问外网的问题
import os
os.environ['disable_fetchurl'] = True

from default_config import *
from config import *

if device_name is None:
  raise Exception(u'please edit this file, specify a device name')


def write_log(location, normal=True):
  content = '{result} , {location} , {time}'.format(
    result='normal' if normal else 'error',
    location=location,
    time=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
  )

  print(content, end='\n', file=sys.stdout if normal else sys.stderr)

  if mail_receiver is not None and mail_smtp is not None:
    send_mail(mail_receiver, "hiki-check {}".format('normal' if normal else 'failed'), content, mail_smtp)
    
  # todo: 发 QQ (twqq) 或短信


def execute(log_when_normal=False):
  """默认只在 error 的情况下写日志，如果想要无论如何都写一条日志（并发邮件和短信），
  可以在调用时把 log_when_normal 设为 True。
  这个功能可以用来确认脚本是否运行正常"""

  resp = requests.get('http://www.hik-online.com/' + device_name, allow_redirects=False)
  location = resp.headers['location']

  try:
    requests.get(location, timeout=connect_timeout)
  except Timeout:
    write_log(location, False)
    return 'error'
  else:
    if log_when_normal:
      write_log(location)
    return 'normal'
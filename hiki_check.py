# -*- coding: utf-8 -*-
from __future__ import print_function
import time
from datetime import datetime
import requests
from requests.exceptions import Timeout
import sys

from default_config import *
from config import *


def write_log(location, normal=True):
  content = '{result} , {location} , {time}'.format(
    result='normal' if normal else 'error',
    location=location,
    time=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
  )
  print(content, end='\n', file=sys.stdout if normal else sys.stderr)

  if not normal:
    # todo： 发邮件、发短信
    pass


if device_name is None:
  raise Exception(u'please edit this file, specify a device name')

while True:
  resp = requests.get('http://www.hik-online.com/' + device_name, allow_redirects=False)
  location = resp.headers['location']

  try:
    requests.get(location, timeout=connect_timeout)
  except Timeout:
    write_log(location, False)
  else:
    write_log(location)

  time.sleep(interval)
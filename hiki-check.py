# -*- coding: utf-8 -*-
import time
from datetime import datetime
import requests
from requests.exceptions import Timeout


device_name = None
interval = 60  # 两次检查间间隔多少秒
connect_timeout = 10 # 通过网络连接目标硬盘录像机允许的时长


def write_log(location, normal=True):
  content = '{result} , {location} , {time}'.format(
    result='normal' if normal else 'error',
    location=location,
    time=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
  )
  
  with open('check.log', 'a') as log_file:
    log_file.write(content + "\n")
  print content


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
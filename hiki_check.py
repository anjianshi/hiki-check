# -*- coding: utf-8 -*-
from datetime import datetime
import requests
from requests.exceptions import Timeout
from flask import Flask
import os
import threading
import time
import smtplib
from email.mime.text import MIMEText


from default_config import *
from config import *

if device_name is None:
  raise Exception(u'please edit this file, specify a device name')


def check(skip_logging=False):
  """执行检查，若发现错误，则写入日志
  把 skip_logging 设为 True 则即使检查失败也不写日志"""

  resp = requests.get('http://www.hik-online.com/' + device_name, allow_redirects=False)
  location = resp.headers['location']

  if _try_connect(location):
    return 'normal'
  else:
    # 如果连接失败，再重试 3 次；在这几次也失败的情况下，才判定是真的无法连接。
    # 这样可以减少误判
    for i in range(3):
      time.sleep(30)
      if _try_connect(location):
        return 'normal'

    if not skip_logging:
      _write_failed_log(location)
    return 'error'


def _try_connect(location):
  try:
    requests.get(location, timeout=connect_timeout)
  except Timeout:
    return False
  else:
    return True


def _write_failed_log(location):
  content = 'check failed, {location} , {time}'.format(
    location=location,
    time=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
  )

  with open('check.log', 'a') as log_file:
    log_file.write(content + "\n")
    _send_mail("hiki-check failed", content)
    _send_sms()


def _send_mail(subject, content):
  """发邮件，必须在 config 文件里指定 mail_receiver 和 mail_smtp 才能发送"""
  if mail_receiver is None or mail_smtp is None:
    return False

  if isinstance(mail_smtp, str):
    mail_account = mail_smtp
    smtp = smtplib.SMTP('localhost')
  else:
    host, port, mail_account, mail_password, use_tls = mail_smtp 
    _cls = smtplib.SMTP_SSL if use_tls else smtplib.SMTP 
    smtp = _cls(host, port)
    smtp.login(mail_account, mail_password)

  msg = MIMEText(unicode(content).encode('utf-8'))
  msg['Subject'] = unicode(subject).encode('utf-8')
  msg['From'] = mail_account
  msg['To'] = mail_receiver
  msg = msg.as_string()

  smtp.sendmail(mail_account, mail_receiver, msg)
  smtp.quit()

  return True


def _send_sms():
  """通过推立方平台(www.tui3.com)发短信，必须在 config 文件里指定 sms_api_key 和 sms_receiver 才能发送
  为避免内容过长被拆分为2条，只给出最简化的通知信息
  """
  if sms_api_key is None or sms_receiver is None:
    return False

  content = sms_template.format('hiki-err')
  if isinstance(content, unicode):
    content = content.encode('utf-8')
  
  resp = requests.post('http://www.tui3.com/api/send/', 
    data=dict(k=sms_api_key, p=1, t=sms_receiver, c=content))
  return True


if __name__ == "__main__":
  # 每隔固定时长进行一次检查
  # 必须在 app 运行前执行，不然无效
  def thread_logic():
    while True:
      print 'result: ' + check()
      time.sleep(check_interval)
  
  threading.Thread(target=thread_logic).start()


  app = Flask(__name__)

  @app.route('/')
  def web_logic():
    """访问此网址会强制执行一次检查，并返回 check.log 中的日志内容"""
    text = 'check result: ' + check(True)

    if os.path.exists('check.log'):
      with open('check.log', 'r') as log_file:
        text += "\n\n\nlog content:\n"
        text += log_file.read()

    return '<pre>' + text + '</pre>'

  app.run(port=app_port)
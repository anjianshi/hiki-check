# -*- coding: utf-8 -*-

app_port = 5000

device_name = None
check_interval = 300 # 两次检查间隔多长时间（单位:秒），默认是5分钟
connect_timeout = 30 # 通过网络连接目标硬盘录像机允许的时长

mail_smtp = None # (host, port, mail_account, mail_password, use_tls) or 'sender_mail_address' for localhost smtp
mail_receiver = None 

sms_api_key = None
sms_receiver = None
sms_template = 't3test {}' # 短信模板，用 {} 做实际信息的占位符。
                           # 推立方短信平台需要对短信内容的格式进行备案。修改此选择来让发出的短信符合备案格式
通过此脚本监控硬盘录像机是否正常运行且联网，一旦出现异常，立即发邮件、短信进行报警（防止有人拉电闸后入室，或者硬盘录像机停机）

目前只支持海康威视硬盘录像机，需要给录像机设置 ddns (访问 http://www.hik-online.com 注册一个账号，然后在硬盘录像机的“网络”栏里进行相关设置)
设置好 ddns 后，修改脚本，指定‘device_name’ （也就是设备名称）

supervisor config:
[program:hiki-check]
command = python hiki_check.py
directory = {{dir_of_this_app}}

nginx config:

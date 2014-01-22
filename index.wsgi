# -*- coding: utf-8 -*-

import sae
from hiki_check import execute

def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, response_headers)

    # 若由 cron 调用，只在 error 时写日志
    # 若是手动调用，则无论如何都写一条日志
    result = execute(environ['QUERY_STRING'] != 'cron=true')

    return ['<strong>Result: {}</strong>'.format(result)]

application = sae.create_wsgi_app(app)


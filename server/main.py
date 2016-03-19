#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ssl
import configparser

from tornado import httpserver, ioloop, netutil, process, web  # , gen
from server.Handlers import MainHandler, APIHandler, AdminHandler


# app's title
__title__ = 'RaspberryPhishServer'


# load configuration from 'configuration.conf' file
config = configparser.ConfigParser()
config.read('configuration.conf')
if 'SERVER' not in config:
    raise ValueError('Please verify your configuration file contains a [SERVER] section')
if 'page_path' not in config['SERVER'] or 'http_port' not in config['SERVER'] or 'https_port' not in config['SERVER']:
    raise ValueError('Please verify [SERVER] section of your configuration file')
# var : directory name where the server will load in 'pages' and 'rsc'
page_path = config['SERVER']['page_path']
http_port = config['SERVER']['http_port']
https_port = config['SERVER']['https_port']


def main():
    print('Starting')
    # create an instance
    application = web.Application([
            (r'/rsc/(.*)', web.StaticFileHandler, {'path': 'rsc/'}),
            (r'/API/(.*)$', APIHandler),
            (r'/admin', AdminHandler),
            (r'/admin/(.*)$', AdminHandler),
            (r'/', MainHandler, dict(page_path=page_path)),
            (r'/.*', MainHandler, dict(page_path=page_path))
        ])
    # HTTP socket
    http_socket = netutil.bind_sockets(http_port)
    # HTTPS socket
    https_socket = netutil.bind_sockets(https_port)
    # fork, except KeyboardInterrupt to properly exit
    try:
        process.fork_processes(0)
    except KeyboardInterrupt:
        ioloop.IOLoop.current().stop()
    # try loading ssl to purpose https
    cert_file = 'cert/' + page_path + 'default.cert'
    key_file = 'cert/' + page_path + 'default.key'
    if os.path.isfile(cert_file) and os.path.isfile(key_file):
        # load ssl requirements
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(cert_file, key_file)
        # bind https port
        print('Start an HTTPS request handler on port : ' + str(https_port))
        httpserver.HTTPServer(application, ssl_options=ssl_ctx).add_sockets(https_socket)
    # bind http port
    print('Start an HTTP request handler on port : ' + str(http_port))
    httpserver.HTTPServer(application).add_sockets(http_socket)
    # loop forever to satisfy user's requests, except KeyboardInterrupt to properly exit
    try:
        ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        ioloop.IOLoop.current().stop()


if __name__ == '__main__':
    main()

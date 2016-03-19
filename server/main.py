#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ssl
import time

import tornado.httpserver
import tornado.ioloop
import tornado.netutil
import tornado.process
import tornado.web
# from tornado import gen

from server.Handlers.MainHandler import MainHandler
from server.Handlers.APIHandler import APIHandler
from server.Handlers.AdminHandler import AdminHandler

# app's title
__title__ = 'RaspberryPhishServer'

# var : directory name where the server will load in 'pages' and 'rsc'
pagePath = 'test/'
http_port = 8080
https_port = 4430


def main():
    # create an instance
    application = tornado.web.Application([
            (r'/rsc/(.*)', tornado.web.StaticFileHandler, {'path': 'rsc/'}),
            (r'/API/(.*)$', APIHandler),
            (r'/admin', AdminHandler),
            (r'/admin/(.*)$', AdminHandler),
            (r'/', MainHandler, dict(page_path=pagePath)),
            (r'/.*', MainHandler, dict(page_path=pagePath))
        ])
    # HTTP socket
    http_socket = tornado.netutil.bind_sockets(http_port)
    # HTTPS socket
    https_socket = tornado.netutil.bind_sockets(https_port)
    # fork, except KeyboardInterrupt to properly exit
    try:
        tornado.process.fork_processes(0)
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.current().stop()
    # try loading ssl to purpose https
    cert_file = 'cert/' + pagePath + 'default.cert'
    key_file = 'cert/' + pagePath + 'default.key'
    if os.path.isfile(cert_file) and os.path.isfile(key_file):
        # load ssl requirements
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(cert_file, key_file)
        # bind https port
        print('Start an HTTPS request handler on port : ' + str(https_port))
        tornado.httpserver.HTTPServer(application, ssl_options=ssl_ctx).add_sockets(https_socket)
    # bind http port
    print('Start an HTTP request handler on port : ' + str(http_port))
    tornado.httpserver.HTTPServer(application).add_sockets(http_socket)
    # loop forever to satisfy user's requests, except KeyboardInterrupt to properly exit
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.current().stop()


if __name__ == '__main__':
    main()

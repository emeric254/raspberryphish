#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ssl
import sys
from tornado import httpserver, ioloop, netutil, web


def start_server(app: web.Application, https_port: int = 443):
    """ Try to start an HTTPS server

    :param app: tornado.web.Application to use
    :param https_port: int the port number to use for HTTPS process
    """
    https_socket = netutil.bind_sockets(https_port)  # HTTPS socket
    # create cert and key file paths
    cert_file = 'cert/default.cert'
    key_file = 'cert/default.key'
    if os.path.isfile(cert_file) and os.path.isfile(key_file):  # verify files
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)  # define ssl context
        ssl_ctx.load_cert_chain(cert_file, key_file)  # load ssl required files
        print('Start an HTTPS request handler on port : ' + str(https_port))  # TODO logger start https
        httpserver.HTTPServer(app, ssl_options=ssl_ctx).add_sockets(https_socket)  # bind https port
    else:
        raise FileNotFoundError  # TODO logger no ssl cert and key files, can't start server
    try:
        ioloop.IOLoop.current().start()  # loop forever to satisfy user's requests
    except KeyboardInterrupt:  # except KeyboardInterrupt to properly exit
        # TODO logger stop and exit
        ioloop.IOLoop.current().stop()  # stop process
        sys.exit(0)  # exit


class BaseHandler(web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

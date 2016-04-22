# -*- coding: utf-8 -*-

import os
import ssl
import sys
from tornado import httpserver, ioloop, netutil, process, web


def start_server(app: web.Application, page_path: str = '', http_port: int = 80, https_port: int = 443):
    """ Try to start as HTTP and HTTPS process as number of threads

    :param app: tornado.web.Application to use in each process
    :param page_path: str defines which folder will be used
    :param http_port: int the port number to use for HTTP process
    :param https_port: int the port number to use for HTTPS process
    """
    http_socket = netutil.bind_sockets(http_port)  # HTTP socket
    https_socket = netutil.bind_sockets(https_port)  # HTTPS socket
    try:
        process.fork_processes(0)  # fork
    except KeyboardInterrupt:  # except KeyboardInterrupt to properly exit
        # TODO logger stop and exit
        ioloop.IOLoop.current().stop()  # stop process
        sys.exit(0)  # exit
    # create cert and key file paths
    cert_file = os.path.join('cert/' + page_path, 'default.cert')
    key_file = os.path.join('cert/' + page_path, 'default.key')
    if os.path.isfile(cert_file) and os.path.isfile(key_file):  # verify files
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)  # define ssl context
        ssl_ctx.load_cert_chain(cert_file, key_file)  # load ssl required files
        print('Start an HTTPS request handler on port : ' + str(https_port))  # TODO logger start https
        httpserver.HTTPServer(app, ssl_options=ssl_ctx).add_sockets(https_socket)  # bind https port
    else:
        pass  # TODO logger no ssl cert and key files
    print('Start an HTTP request handler on port : ' + str(http_port))  # TODO logger start http
    httpserver.HTTPServer(app).add_sockets(http_socket)  # bind http port
    try:
        ioloop.IOLoop.current().start()  # loop forever to satisfy user's requests
    except KeyboardInterrupt:  # except KeyboardInterrupt to properly exit
        # TODO logger stop and exit
        ioloop.IOLoop.current().stop()  # stop process
        sys.exit(0)  # exit

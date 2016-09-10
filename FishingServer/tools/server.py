# -*- coding: utf-8 -*-

import os
import ssl
import sys
import logging
from tornado import httpserver, ioloop, netutil, process, web
from tools import ConfLoader


def stop_server():
    """Stop server IOLoop and forked processes"""
    logging.info('Stopping and exiting all server processes ...')
    ioloop.IOLoop.current().stop()
    sys.exit(0)  # exit properly


def start_server(app: web.Application):
    """ Try to start as HTTP and HTTPS process as number of threads.

    :param app: tornado.web.Application to use in all processes

    """
    (cert_path, http_port, https_port) = ConfLoader.load_server_conf()  # load configuration
    http_socket = netutil.bind_sockets(http_port)  # bind HTTP socket
    https_socket = netutil.bind_sockets(https_port)  # bind HTTPS socket
    cert_file = os.path.join(cert_path, 'default.crt')  # ssl cert file
    key_file = os.path.join(cert_path, 'default.key')  # ssl key file
    try:
        logging.debug('Trying to fork into multiple processes')
        process.fork_processes(0)  # fork in N processes
    except KeyboardInterrupt:  # except KeyboardInterrupt to properly exit
        stop_server()
    if os.path.isfile(cert_file) and os.path.isfile(key_file):  # verify files
        logging.info('Required cert and key files found, loading them')
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)  # define ssl context
        ssl_ctx.load_cert_chain(cert_file, key_file)  # load ssl required files
        logging.info('Starting an HTTPS request handler on port : ' + str(https_port))
        httpserver.HTTPServer(app, ssl_options=ssl_ctx).add_sockets(https_socket)  # add socket to https port
    else:  # no ssl files found
        logging.warning('No cert and key files found, HTTPS service will not start.')
    logging.info('Starting an HTTP request handler on port : ' + str(http_port))
    httpserver.HTTPServer(app).add_sockets(http_socket)  # add socket to http port
    try:
        ioloop.IOLoop.current().start()  # loop forever to satisfy user's requests
    except KeyboardInterrupt:  # except KeyboardInterrupt to properly exit
        stop_server()

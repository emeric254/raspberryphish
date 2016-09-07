#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ssl
import sys
import logging
from tornado import httpserver, ioloop, netutil, web, escape
from tools import ConfLoader

(cert_path, https_port) = ConfLoader.load_server_conf()
(login, password, max_attempts, blocked_duration) = ConfLoader.load_login_conf()


def start_server(app: web.Application):
    """ Try to start an HTTPS AdminServer

    :param app: tornado.web.Application to use

    """
    https_socket = netutil.bind_sockets(https_port)  # HTTPS socket
    # create cert and key file paths
    cert_file = os.path.join(cert_path, 'default.crt')
    key_file = os.path.join(cert_path, 'default.key')
    if os.path.isfile(cert_file) and os.path.isfile(key_file):  # verify files
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)  # define ssl context
        ssl_ctx.load_cert_chain(cert_file, key_file)  # load ssl required files
        logging.info('Starting an HTTPS request handler on port : ' + str(https_port))
        httpserver.HTTPServer(app, ssl_options=ssl_ctx).add_sockets(https_socket)  # bind https port
    else:
        logging.error('No ssl cert and / or key files, aborting ...')
        raise FileNotFoundError
    try:
        ioloop.IOLoop.current().start()  # loop forever to satisfy user's requests
    except KeyboardInterrupt:  # except KeyboardInterrupt to properly exit
        logging.info('Exiting an HTTPS request handler on port : ' + str(https_port))
        ioloop.IOLoop.current().stop()  # stop process
        sys.exit(0)  # exit


class BaseSecureHandler(web.RequestHandler):
    """Superclass for Handlers which require a connected user"""

    def get_current_user(self):
        """Get current connected user

        :return: current connected user

        """
        return self.get_secure_cookie('user')


class LoginHandler(BaseSecureHandler, ):
    """Handle user login actions"""

    def initialize(self, cookie_expiration: int = 1):
        """Set cookie expiration value to a value loaded from the main method"""
        self.cookie_expiration = cookie_expiration

    def get(self):
        """Get login form"""
        incorrect = self.get_secure_cookie('incorrect')
        if incorrect and int(incorrect) > max_attempts:
            logging.warning('an user have been blocked')
            self.render('blocked.html', blocked_duration=blocked_duration)
            return
        self.render('login.html', user=self.current_user, failed=False)

    def post(self):
        """Post connection form and try to connect with these credentials"""
        get_username = escape.xhtml_escape(self.get_argument('username'))
        get_password = escape.xhtml_escape(self.get_argument('password'))
        if login == get_username and password == get_password:
            self.set_secure_cookie('user', self.get_argument('username'), expires_days=self.cookie_expiration)
            self.set_secure_cookie('incorrect', '0')
            self.redirect('/')
        else:
            logging.info('invalid credentials')
            incorrect = self.get_secure_cookie('incorrect')
            if not incorrect:
                incorrect = 0
            self.set_secure_cookie('incorrect', str(int(incorrect) + 1), expires_days=self.cookie_expiration)
            self.render('login.html', user=self.current_user, failed=True)


class LogoutHandler(BaseSecureHandler):
    """Handle user logout action"""

    def get(self):
        """Disconnect an user, delete his cookie and redirect him"""
        self.clear_cookie('user')
        self.redirect('/')

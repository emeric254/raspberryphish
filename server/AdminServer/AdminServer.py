#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ssl
import sys
import time
import base64
import configparser
from tornado import httpserver, ioloop, netutil, web, escape


# app's title
__title__ = 'RaspberryPhishServer'


# load configuration
config = configparser.ConfigParser()
config.read('configuration.conf')  # load configuration from 'configuration.conf' file
if 'SERVER' not in config:
    raise ValueError('Please verify [configuration.conf] contains a [SERVER] section')
if 'https_port' not in config['SERVER']\
        or 'login' not in config['SERVER']\
        or 'password' not in config['SERVER']\
        or 'cookie_secret' not in config['SERVER']:
    raise ValueError('Please verify [SERVER] section in [configuration.conf]')
https_port = config['SERVER']['https_port']  # HTTPS port to bind
login = config['SERVER']['login']
password = config['SERVER']['password']
cookie_secret = config['SERVER']['cookie_secret']
if not https_port or not login or not password or not cookie_secret:
    raise ValueError('Please verify values in [configuration.conf]')


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


class AdminHandler(BaseHandler):
    """AdminHandler handle /rsc endpoint

    GET give the rsc page
    POST try to execute a received action
    """

    @web.asynchronous
    @web.authenticated
    async def get(self):
        # self.render('../pages/rsc/index.html', user=self.current_user)
        with open('./index.html', mode='r', encoding='UTF-8') as page:
            self.write(page.read())

    @web.asynchronous
    @web.authenticated
    def post(self):
        try:
            # TODO do something with this ?!
            arguments = {}
            for k in self.request.arguments:
                arguments[k] = self.get_argument(k)
            print('arguments :', arguments)
        except web.HTTPError:   # no or wrong arguments
            pass
        # self.render('../pages/rsc/index.html')
        with open('./index.html', mode='r', encoding='UTF-8') as page:
            self.write(page.read())


class LoginHandler(BaseHandler):
    @web.asynchronous
    def get(self):
        incorrect = self.get_secure_cookie("incorrect")
        if incorrect and int(incorrect) > 25:
            self.write('<center>blocked</center>')
            return
        self.render('./login.html', user=self.current_user)

    @web.asynchronous
    def post(self):
        getusername = escape.xhtml_escape(self.get_argument("username"))
        getpassword = escape.xhtml_escape(self.get_argument("password"))
        if login == getusername and password == getpassword:
            self.set_secure_cookie("user", self.get_argument("username"))
            self.set_secure_cookie("incorrect", "0")
            self.redirect('/admin')
        else:
            incorrect = self.get_secure_cookie("incorrect")
            if not incorrect:
                incorrect = 0
            self.set_secure_cookie('incorrect', str(int(incorrect) + 1))
            self.render('./login.html', user=self.current_user)


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect('/')


def main():
    """Main function, define an Application and start server instances with it.
    """

    # define Application endpoints
    application = web.Application([
            (r'/rsc/(.*)', web.StaticFileHandler, {'path': 'rsc/'}),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
            # (r'/API/(.*)$', APIHandler),
            (r'/', AdminHandler),
            (r'/.*', AdminHandler)
        ])

    application.settings = {
            'cookie_secret': cookie_secret,
            'login_url': '/login',
            'debug': True,
        }

    # start server with this Application and previously loaded parameters
    start_server(application, https_port)


if __name__ == '__main__':
    main()  # execute main function

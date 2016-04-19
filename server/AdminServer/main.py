#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import random
import string
from tornado import web, escape
from APIHandler import APIHandler
from AdminHandler import AdminHandler
import server

# app's title
__title__ = 'RaspberryPhishAdminServer'


# load configuration
config = configparser.ConfigParser()
config.read('configuration.conf')  # load configuration from 'configuration.conf' file

# missing section ?
if 'SERVER' not in config:
    raise ValueError('Please verify [configuration.conf] contains a [SERVER] section')

# missing a value ?
if 'https_port' not in config['SERVER'] or 'login' not in config['SERVER'] \
        or 'password' not in config['SERVER'] or 'cookie_secret' not in config['SERVER']:
    raise ValueError('Please verify [SERVER] section in [configuration.conf]')

# get configuration values
https_port = config['SERVER']['https_port']  # HTTPS port to bind
login = config['SERVER']['login']  # login for admin
password = config['SERVER']['password']  # password for admin
cookie_secret = config['SERVER']['cookie_secret']  # hash to create cookies

debug = False
if 'debug' in config['SERVER'] and isinstance(config['SERVER']['debug'], bool):
    debug = config['SERVER']['debug']
autoreload = False
if 'autoreload' in config['SERVER'] and isinstance(config['SERVER']['autoreload'], bool):
    autoreload = config['SERVER']['autoreload']

# invalid configuration ?
if not https_port or not login or not password or not cookie_secret \
        or int(https_port) < 1 or int(https_port) > 65535 \
        or len(login) < 1 or len(password) < 1 or len(cookie_secret) < 1:
    raise ValueError('Please verify values in [configuration.conf]')


class LoginHandler(server.BaseHandler):
    # TODO doc
    @web.asynchronous
    def get(self):
        # TODO doc
        incorrect = self.get_secure_cookie("incorrect")
        if incorrect and int(incorrect) > 25:
            self.write('<center>blocked</center>')
            return
        self.render('login.html', user=self.current_user)

    @web.asynchronous
    def post(self):
        # TODO doc
        getusername = escape.xhtml_escape(self.get_argument("username"))
        getpassword = escape.xhtml_escape(self.get_argument("password"))
        if login == getusername and password == getpassword:
            self.set_secure_cookie("user", self.get_argument("username"), expires_days=1)
            self.set_secure_cookie("incorrect", "0")
            self.redirect('/')
        else:
            incorrect = self.get_secure_cookie("incorrect")
            if not incorrect:
                incorrect = 0
            self.set_secure_cookie('incorrect', str(int(incorrect) + 1))
            self.render('login.html', user=self.current_user)


class LogoutHandler(server.BaseHandler):
    # TODO doc
    @web.asynchronous
    def get(self):
        # TODO doc
        self.clear_cookie('user')
        self.redirect('/')


def main():
    """Main function, define an Application and start server instances with it.
    """
    # define settings (static path / login / cookies / debug)
    settings = {
        'static_path': 'static',
        'cookie_secret': cookie_secret.join([random.choice(string.printable) for _ in range(24)]),
        'xsrf_cookies': True,
        'login_url': '/login',
        'debug': debug,
        'autoreload': autoreload
    }
    # define Application endpoints
    application = web.Application([
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
            (r'/api/(.*)$', APIHandler),
            (r'/', AdminHandler)
        ], **settings)
    # start server with this Application and previously loaded parameters
    server.start_server(application, https_port=https_port)


if __name__ == '__main__':
    main()  # execute main function

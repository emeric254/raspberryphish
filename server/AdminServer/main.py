#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import ConfLoader
import server
from tornado import web, escape
from APIHandler import APIHandler
from AdminHandler import AdminHandler

# app's title
__title__ = 'RaspberryPhishAdminServer'

logging.basicConfig(filename='serveur.log', level=logging.INFO)

(
    https_port,
    login,
    password,
    cookie_secret,
    debug,
    autoreload,
    max_attemps,
    blocked_duration
) = ConfLoader.load_conf(conf_file='configuration.conf')


class LoginHandler(server.BaseHandler):
    """Handle user login actions
    """
    @web.asynchronous
    def get(self):
        """Get login form
        """
        incorrect = self.get_secure_cookie("incorrect")
        if incorrect and int(incorrect) > max_attemps:
            logging.warning('an user have been blocked')
            self.render('blocked.html', blocked_duration=blocked_duration)
            return
        self.render('login.html', user=self.current_user, failed=False)

    @web.asynchronous
    def post(self):
        """Post connection form and try to connect with these credentials
        """
        getusername = escape.xhtml_escape(self.get_argument("username"))
        getpassword = escape.xhtml_escape(self.get_argument("password"))
        if login == getusername and password == getpassword:
            self.set_secure_cookie("user", self.get_argument("username"), expires_days=1)
            self.set_secure_cookie("incorrect", "0")
            self.redirect('/')
        else:
            logging.info('invalid credentials')
            incorrect = self.get_secure_cookie("incorrect")
            if not incorrect:
                incorrect = 0
            self.set_secure_cookie('incorrect', str(int(incorrect) + 1), expires_days=1)
            self.render('login.html', user=self.current_user, failed=True)


class LogoutHandler(server.BaseHandler):
    """Handle user logout action
    """
    @web.asynchronous
    def get(self):
        """Disconnect an user, delete his cookie and redirect him
        """
        self.clear_cookie('user')
        self.redirect('/')


def main():
    """Main function, define an Application and start server instances with it.
    """
    # define app settings
    settings = {
        'static_path': './static',
        'template_path': './templates',
        'cookie_secret': cookie_secret,
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
    # start a server running this Application with these loaded parameters
    server.start_server(application)


if __name__ == '__main__':
    main()  # execute main function

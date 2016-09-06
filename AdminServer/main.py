#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from tornado import web, escape
from tools import ConfLoader, server
from Handlers import APIHandler, AdminHandler


class LoginHandler(server.BaseSecureHandler):
    """Handle user login actions"""

    def get(self):
        """Get login form"""
        incorrect = self.get_secure_cookie("incorrect")
        if incorrect and int(incorrect) > max_attemps:
            logging.warning('an user have been blocked')
            self.render('blocked.html', blocked_duration=blocked_duration)
            return
        self.render('login.html', user=self.current_user, failed=False)

    def post(self):
        """Post connection form and try to connect with these credentials"""
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


def main():
    """Main function, define an Application and start AdminServer instances with it."""
    settings = {
        'static_path': './static',
        'template_path': './templates',
        'cookie_secret': cookie_secret,
        'xsrf_cookies': True,
        'login_url': '/login',
        'debug': debug,
        'autoreload': autoreload
    }
    application = web.Application([
            (r'/login', LoginHandler),
            (r'/logout', server.LogoutHandler),
            (r'/api/(.*)$', APIHandler.APIHandler),
            (r'/', AdminHandler.AdminHandler)
        ], **settings)
    server.start_server(application)  # start a AdminServer running this Application with these loaded parameters


if __name__ == '__main__':
    logging.basicConfig(filename='serveur.log', level=logging.INFO)
    (
        login,
        password,
        cookie_secret,
        debug,
        autoreload,
        max_attemps,
        blocked_duration
    ) = ConfLoader.load_conf()
    main()  # execute main function

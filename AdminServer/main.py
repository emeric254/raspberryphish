#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from tornado import web, escape
from tools import ConfLoader, server
from Handlers import APIHandler, AdminHandler


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
            (r'/login', server.LoginHandler, dict(cookie_expiration=cookie_expiration)),
            (r'/logout', server.LogoutHandler),
            (r'/api/(.*)$', APIHandler.APIHandler),
            (r'/', AdminHandler.AdminHandler)
        ], **settings)
    server.start_server(application)  # start a AdminServer running this Application with these loaded parameters


if __name__ == '__main__':
    logging.basicConfig(filename='serveur.log', level=logging.INFO)
    (debug, autoreload) = ConfLoader.load_conf()
    (cookie_expiration, cookie_secret) = ConfLoader.load_cookie_conf()
    main()  # execute main function

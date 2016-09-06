# -*- coding: utf-8 -*-

from tornado import web
from tools import server


class AdminHandler(server.BaseSecureHandler):
    """AdminHandler handle /static endpoint"""

    @web.asynchronous
    @web.authenticated
    def get(self):
        """Render main page"""
        # TODO logging
        self.render('./admin.html')

    @web.asynchronous
    @web.authenticated
    def post(self):
        """Do something with arguments and render main page"""
        # TODO logging
        try:
            # TODO do something here with argument(s) ?!
            arguments = {}
            for k in self.request.arguments:
                arguments[k] = self.get_argument(k)
            print('arguments :', arguments)
        except web.HTTPError:   # no or wrong arguments
            pass  # TODO logging
        self.render('admin.html')

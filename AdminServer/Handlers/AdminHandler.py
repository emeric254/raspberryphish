# -*- coding: utf-8 -*-

import logging
from tornado import web
from tools import server


class AdminHandler(server.BaseSecureHandler):
    """AdminHandler handle /static endpoint"""

    @web.authenticated
    def get(self):
        """Render main page"""
        logging.info(str(self.get_current_user()) + ' made a GET on AdminHandler')
        self.render('admin.html')

    @web.authenticated
    def post(self):
        """Do something with arguments and render main page"""
        logging.info(str(self.get_current_user()) + ' made a POST on AdminHandler')
        try:
            arguments = {}
            for k in self.request.arguments:
                arguments[k] = self.get_argument(k)
            # TODO do something here with argument(s) ?!
            logging.debug('arguments :' + str(arguments))
        except web.HTTPError:   # no or wrong arguments
            logging.warning('Argument error on AdminHandler POST request')
        self.render('admin.html')

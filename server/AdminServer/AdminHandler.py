# -*- coding: utf-8 -*-

from tornado import web
import server


class AdminHandler(server.BaseHandler):
    """AdminHandler handle /static endpoint

    GET give the static page
    POST try to execute a received action
    """
    @web.asynchronous
    @web.authenticated
    async def get(self):
        # TODO doc
        self.render('./admin.html')

    @web.asynchronous
    @web.authenticated
    def post(self):
        # TODO doc
        try:
            # TODO do something with this ?!
            arguments = {}
            for k in self.request.arguments:
                arguments[k] = self.get_argument(k)
            print('arguments :', arguments)
        except web.HTTPError:   # no or wrong arguments
            pass
        self.render('admin.html')

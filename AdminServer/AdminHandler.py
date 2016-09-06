# -*- coding: utf-8 -*-

from tornado import web

from AdminServer import server


class AdminHandler(server.BaseHandler):
    """AdminHandler handle /static endpoint

    GET give the static page
    POST try to execute a received action
    """
    @web.asynchronous
    @web.authenticated
    async def get(self):
        """Render main page
        """
        self.render('./admin.html')

    @web.asynchronous
    @web.authenticated
    def post(self):
        """Do something with arguments and render main page
        """
        try:
            # TODO do something here with argument(s) ?!
            arguments = {}
            for k in self.request.arguments:
                arguments[k] = self.get_argument(k)
            print('arguments :', arguments)
        except web.HTTPError:   # no or wrong arguments
            pass
        self.render('admin.html')

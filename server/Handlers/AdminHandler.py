# -*- coding: utf-8 -*-

from tornado import web


class AdminHandler(web.RequestHandler):
    """AdminHandler handle /admin endpoint

    GET give the admin page
    POST try to execute a received action
    """

    @web.asynchronous
    async def data_received(self, chunk):
        pass

    @web.asynchronous
    async def get(self):
        # self.render('../pages/admin/index.html')
        with open('./pages/admin/index.html', mode='r', encoding='UTF-8') as page:
            self.write(page.read())

    def post(self):
        try:
            action = self.get_argument('action')
            # TODO do something with this ?!
            print('action :', action)
        except web.HTTPError:   # no or wrong arguments
            pass
        # self.render('../pages/admin/index.html')
        with open('./pages/admin/index.html', mode='r', encoding='UTF-8') as page:
            self.write(page.read())

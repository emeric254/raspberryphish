# -*- coding: utf-8 -*-

from tornado import web  # , gen


class AdminHandler(web.RequestHandler):
    @web.asynchronous
    # @gen.coroutine
    async def data_received(self, chunk):
        pass

    @web.asynchronous
    # @gen.coroutine
    async def get(self):
        self.render('../pages/admin/index.html')

    def post(self):
        try:
            action = self.get_argument('action')
            print('action :', action)
        except web.HTTPError:   # no or wrong arguments
            pass
        self.render('../pages/admin/index.html')

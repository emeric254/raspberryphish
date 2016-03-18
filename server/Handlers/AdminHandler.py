# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
# from tornado import gen


class AdminHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    # @gen.coroutine
    async def data_received(self, chunk):
        pass

    @tornado.web.asynchronous
    # @gen.coroutine
    async def get(self):
        self.render('../pages/admin/index.html')

    def post(self):
        try:
            action = self.get_argument('action')
            print('action :', action)
        except tornado.web.HTTPError:   # no or wrong arguments
            pass
        self.render('../pages/admin/index.html')

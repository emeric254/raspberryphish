#!/usr/bin/env python
# -*- coding: utf-8 -*-

import server
from tornado import web
from Handlers import MainHandler, APIHandler, AdminHandler
from Tools import ConfLoader


# app's title
__title__ = 'RaspberryPhishServer'


def main():
    """Main function, define an Application and start server instances with it.
    """

    # load parameters from configuration file
    (page_path, http_port, https_port) = ConfLoader.load_server_conf()

    # define Application endpoints
    application = web.Application([
            (r'/rsc/(.*)', web.StaticFileHandler, {'path': 'rsc/'}),
            (r'/API/(.*)$', APIHandler),
            (r'/admin', AdminHandler),
            (r'/admin/(.*)$', AdminHandler),
            (r'/', MainHandler, dict(page_path=page_path)),
            (r'/.*', MainHandler, dict(page_path=page_path))
        ])

    # start server with this Application and previously loaded parameters
    server.start_server(application, page_path, http_port, https_port)


if __name__ == '__main__':
    main()  # execute main function

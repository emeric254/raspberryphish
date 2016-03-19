# -*- coding: utf-8 -*-

import os
import time
import random
import json
import tornado.ioloop
import tornado.web
# from tornado import gen

from server.Modules.UnixSysInfos import OSInfos, CpuInfos, StorageInfos, RamInfos, SensorInfos


def liste_dump(folder):
    dico = {}
    for root, _, files in os.walk(folder):
        for dump in files:
            path = "./" + root + "/" + dump
            dico[dump] = open(path).read().replace("login:", "").replace("password:", "").split("\n")[:-1]
    return dico


# Handler for ressources
class APIHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    # @gen.coroutine
    async def data_received(self, chunk):
        pass

    @tornado.web.asynchronous
    # @gen.coroutine
    async def get(self, path_request):
        if path_request == "timestamp":
            self.write(str(time.time()))
        elif path_request == "random":
            try:
                maximum = int(self.get_argument('max'))
            except ValueError:
                maximum = 100
            try:
                minimum = int(self.get_argument('min'))
            except ValueError:
                minimum = 0
            self.write(str(random.randint(minimum, maximum)))
        elif path_request == "system/info":
            self.write(
                json.dumps(
                    {
                        "OS":
                            {
                                "Name": OSInfos.os_name(),
                                "Host": OSInfos.name(),
                                "Python": OSInfos.python_version(),
                                "Interpreter": OSInfos.interpreter_name()
                            },
                        "CPU":
                            {
                                "Type": CpuInfos.cpu_type(),
                                "Name": CpuInfos.cpu_name()
                            }
                        # TODO continue
                    }
                )
            )
        elif path_request == "system/load":
            self.write(
                json.dumps(
                    {
                        "CPU": CpuInfos.avg_load(),
                        "RAM": RamInfos.avg_load(),
                        "Storage": StorageInfos.avg_load()
                        # TODO continue
                    }
                )
            )
        elif path_request == "system/sensor":
            self.write(
                json.dumps(
                    {
                        "CPU": SensorInfos.cpu_temp(),
                        "MB": SensorInfos.mb_temp(),
                        # "Storage": SensorInfos.hdd_temp()
                        # TODO continue
                    }
                )
            )
        elif path_request == "dump":
            self.write(json.dumps(liste_dump("logs/dump")))
        elif path_request.startswith("dump/"):
            path = "logs/" + path_request
            try:
                if os.path.isfile(path):
                    self.write(open(path).read())
                else:
                    self.write("not found : " + path)
            except FileNotFoundError:
                self.write("error [file not found] : " + path)

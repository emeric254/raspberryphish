
import os
import time
import random
import json
import tornado.ioloop, tornado.web
from tornado import gen
from Modules.UnixSysInfos import *


def liste_dump(folder):
    dico = {}
    for root, dirs, files in os.walk(folder):
        for dump in files:
            path = "./" + root + "/" + dump
            dico[dump] = open(path).read().replace("login:", "").replace("password:", "").split("\n")[:-1]
    return dico


# Handler for ressources
class APIHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    #@gen.coroutine
    async def get(self, path_request):
        if path_request == "timestamp":
            self.write(str(time.time()))
        elif path_request == "random":
            try:
                maximum = int(self.get_argument('max'))
            except:
                maximum = 100
            try:
                minimum = int(self.get_argument('min'))
            except:
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
                        #@TODO continue
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
                        #@TODO continue
                    }
                )
            )
        elif path_request == "system/sensor":
            self.write(
                json.dumps(
                    {
                        "CPU": SensorInfos.cpu_temp(),
                        "MB": SensorInfos.mb_temp(),
                        "Storage": SensorInfos.hdd_temp()
                        #@TODO continue
                    }
                )
            )
        elif path_request == "dump":
            self.write(json.dumps(liste_dump("logs/dump")))
        elif path_request.startswith("dump/"):
            try:
                if os.path.isfile("logs/" + path_request):
                    self.write(open(path).read())
                else:
                    self.write("not found")
            except:
                self.write("error")


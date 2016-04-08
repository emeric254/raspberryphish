# -*- coding: utf-8 -*-

import os
import time
import random
import json

from tornado import web
from Modules.UnixSysInfos import OSInfos, CpuInfos, StorageInfos, RamInfos, SensorInfos


def system_infos():
    return {
        'OS': {
            'Name': OSInfos.os_name(),
            'Host': OSInfos.name(),
            'Python': OSInfos.python_version(),
            'Interpreter': OSInfos.interpreter_name()
        },
        'CPU': {
            'Type': CpuInfos.cpu_type(),
            'Name': CpuInfos.cpu_name()
        }
        # TODO continue
    }


def system_load():
    return {
        'CPU': CpuInfos.avg_load(),
        'RAM': RamInfos.avg_load(),
        'Storage': StorageInfos.avg_load()
        # TODO continue
    }


def system_sensors():
    return {
        'CPU': SensorInfos.cpu_temp(),
        'MB': SensorInfos.mb_temp()
        # 'Storage': SensorInfos.hdd_temp()
        # TODO continue
    }


def del_dump(folder: str = '../logs/dump'):
    print('deleting ' + folder)
    for root, folders, files in os.walk(folder):
        for temp in files:
            path = root + '/' + temp
            print('delete file ' + path)
            os.remove(path)
        for temp in folders:
            path = root + '/' + temp
            print('delete folder ' + path)
            os.rmdir(path)
    os.rmdir(folder)


def liste_dump(folder: str = '../logs/dump'):
    dico = {}
    for root, _, files in os.walk(folder):
        for dump in files:
            path = root + '/' + dump
            (login, passwd) = open(path).read().replace('login:', '').replace('password:', '').split('\n')[:-1]
            entry = root[8:]
            if entry not in dico:
                dico[entry] = {}
            dico[entry][dump] = [login, passwd]
    return dico


class APIHandler(web.RequestHandler):
    """APIHandler exposes various API endpoints
    """

    @web.asynchronous
    async def data_received(self, chunk):
        pass

    @web.asynchronous
    async def get(self, path_request):
        if path_request == 'timestamp':
            self.write(str(time.time()))
        elif path_request == 'random':
            self.api_random()
        elif path_request == 'system/info':
            self.write(json.dumps(system_infos()))
        elif path_request == 'system/load':
            self.write(json.dumps(system_load()))
        elif path_request == 'system/sensor':
            self.write(json.dumps(system_sensors()))
        elif path_request == 'dump':
            self.write(json.dumps(liste_dump()))
        elif path_request.startswith('dump/'):
            path = '../logs/' + path_request
            try:
                if os.path.isfile(path):
                    with open(path, mode='r', encoding='UTF-8') as file:
                        self.write(file.read())
                elif os.path.isdir(path):
                    self.write(json.dumps(liste_dump(path)))
                else:
                    self.write('not found : ' + path[8:])
            except FileNotFoundError:
                self.write('error [file not found] : ' + path[8:])

    def delete(self, path_request):
        if path_request == 'dump':
            del_dump()
            self.write('ok')
        elif path_request.startswith('dump/'):
            path = '../logs/' + path_request
            try:
                del_dump(path)
                self.write('ok')
            except FileNotFoundError:
                self.send_error(status_code=404, reason='not found : ' + path[8:])

    def api_random(self):
        try:
            maximum = int(self.get_argument('max', default=100))
        except ValueError:
            maximum = 100
        try:
            minimum = int(self.get_argument('min', default=0))
        except ValueError:
            minimum = 0
        self.write(str(random.randint(minimum, maximum)))

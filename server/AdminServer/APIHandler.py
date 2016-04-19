# -*- coding: utf-8 -*-

import os
import time
import random
import json
from tornado import web
import server


def del_dump(folder: str = '../logs/dump'):
    # TODO doc
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
    # TODO doc
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


class APIHandler(server.BaseHandler):
    """APIHandler exposes various API endpoints
    """
    @web.asynchronous
    @web.authenticated
    async def get(self, path_request):
        # TODO doc
        if path_request == 'timestamp':
            self.write(str(time.time()))
        elif path_request == 'random':
            try:
                maximum = int(self.get_argument('max', default=100))
            except ValueError:
                maximum = 100
            try:
                minimum = int(self.get_argument('min', default=0))
            except ValueError:
                minimum = 0
            self.write(str(random.randint(minimum, maximum)))
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

    @web.authenticated
    def delete(self, path_request):
        # TODO doc
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

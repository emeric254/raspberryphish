# -*- coding: utf-8 -*-

import os
import time
import json
import random
import logging
from tornado import web
from tools import server, FileManager


def liste_dump(folder: str):
    """List dump entries from a folder

    :param folder: folder to list dumps
    :return: dumps entries

    """
    dico = {}
    for root, _, files in os.walk(folder):
        for dump in files:
            path = os.path.join(root, dump)
            (login, passwd) = open(path).read().replace('login:', '').replace('password:', '').split('\n')[:-1]
            entry = root[8:]
            if entry not in dico:
                dico[entry] = {}
            dico[entry][dump] = [login, passwd]
    return dico


class APIHandler(server.BaseSecureHandler):
    """APIHandler exposes various API endpoints"""

    @web.authenticated
    def get(self, path_request):
        """API get details of something

        :param path_request: URI representing something to get details

        """
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
        elif path_request == 'dumps':
            self.write(json.dumps(liste_dump('../logs/dump')))
        elif path_request.startswith('dumps/'):
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
        """API delete something

        :param path_request: URI representing something to delete

        """
        if path_request == 'dumps':  # delete all subfolders and '../logs/dump'
            FileManager.del_folder('../logs/dump')
            self.write('ok')
        elif path_request.startswith('dumps/'):  # delete a subfolder of '../logs/dump'
            path = '../logs/' + path_request
            try:
                FileManager.del_folder(path)
                self.write('ok')
            except FileNotFoundError:
                self.send_error(status_code=404, reason='not found : ' + path[8:])

# -*- coding: utf-8 -*-

import os


class Log:
    # TODO doc

    def __init__(self, folder, login, tries=None):
        self.folder = folder
        self.login = login
        if tries:
            self.tries = tries
        else:
            self.tries = {}

    def getfolder(self):
        # TODO doc
        return self.folder

    def getlogin(self):
        # TODO doc
        return self.login

    def gettries(self):
        # TODO doc
        return self.tries

    def addtry(self, timestamp, password, test):
        # TODO doc
        self.tries[timestamp] = (password, test)

    def edittry(self, timestamp, password, test):
        # TODO doc
        self.tries[timestamp] = (password, test)

    def __str__(self):
        chaine = self.getfolder() + " > " + self.getlogin()
        for timestamp, value in self.tries.items():
            chaine += ("\n>>" + str(timestamp) + " @ " + str(value))
        return chaine


def dump_list(folder):
    # TODO doc
    dico = {}
    for root, _, files in os.walk(folder):
        for dump_file in files:
            dico[dump_file] = ()
            path = "./" + root + "/" + dump_file
            print(open(path).read().replace("login:", "").replace("password:", "").split("\n")[:-1])
    return dico

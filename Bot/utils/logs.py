#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class Log:
    def __init__(self, folder, login, tries=None, tested=False):
        self.folder = folder
        self.login = login
        if tries:
            self.tries = tries
        else:
            self.tries = {}

    def getfolder(self):
        return self.folder

    def getlogin(self):
        return self.login

    def gettries(self):
        return self.tries

    def addtry(self, timestamp, password, test):
        self.tries[timestamp] = (password, test)

    def edittry(self, timestamp, password, test):
        self.tries[timestamp] = (password, test)

    def __str__(self):
        chaine = self.getfolder() + " > " + self.getlogin()
        for timestamp, value in self.tries.items():
            chaine += ("\n>>" + str(timestamp) + " @ " + str(value))
        return chaine


def liste_dump(folder):
    dico = {}
    for root, dirs, files in os.walk(folder):
        for dump in files:
            path = "./" + root + "/" + dump
            print(open(path).read().replace("login:", "").replace("password:", "").split("\n")[:-1])
            dico[dump] = ()
    return dico

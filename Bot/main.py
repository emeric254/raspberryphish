#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import connect

__title__ = "Bot"


to_test = []     # dumps which have to be tested
tested = {}     # don't try same (login, password) more than one time


for l in to_test:
    login = l.getlogin()
    tries = l.gettries()
    for timestamp in tries:
        password, test = tries[timestamp]
        if login not in tested or password not in tested[login]:
            (result, identity) = connect.tryconnection(login, password)
            if result:
                # print(identity)
                l.edittry(timestamp, password, True)
            else:
                l.edittry(timestamp, password, False)
            if login not in tested:
                tested[login] = []
            tested[login].append(password)

print(tested)
for l in to_test:
    print(l)

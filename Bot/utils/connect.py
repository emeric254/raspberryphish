#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


# for example "ups" identities test :
def tryconnection(login, password):
    # request with args
    args = {'loginbtn': 'Login', 'rememberusername': '1', 'username': login, 'password': password}
    r = requests.post("https://moodle.univ-tlse3.fr/login/index.php", args)
    # parsing
    soup = BeautifulSoup(r.text, "lxml")
    # try to find error message
    result = soup.find_all(id='loginerrormessage')
    if not result:
        # success
        result = soup.find_all(id='page-header-wrapper')
        if result:
            # parsing to find identity
            result = BeautifulSoup(str(result[0]), 'lxml')
            identity = result.a.string

            # disconnect
            #r = requests.get(resultat.a.next_sibling.next_sibling['href'])

            # return
            return True, identity
    # return
    return False, None

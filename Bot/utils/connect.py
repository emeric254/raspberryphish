# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def moodle_connection(login, password):  # "ups" credentials test
    # TODO doc
    args = {'loginbtn': 'Login', 'rememberusername': '1', 'username': login, 'password': password}
    r = requests.post("https://moodle.univ-tlse3.fr/login/index.php", args)  # request with args
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "lxml")  # parsing
        if not soup.find_all(id='loginerrormessage'):  # no error message found
            result = soup.find_all(id='page-header-wrapper')
            if result:
                identity = BeautifulSoup(str(result[0]), 'lxml').a.string  # parsing to find identity
                # r = requests.get(resultat.a.next_sibling.next_sibling['href'])  # disconnect
                return identity  # return found identity
    return None  # return nothing
